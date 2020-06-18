"""
Functionality for generating grade reports.
"""
import logging
import re
from collections import OrderedDict
from datetime import datetime
from itertools import chain, izip, izip_longest
from time import time

from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import ugettext as _
from lazy import lazy
from opaque_keys.edx.keys import UsageKey
from pytz import UTC
from six import text_type

from course_blocks.api import get_course_blocks
from courseware.courses import get_course_by_id
from courseware.user_state_client import DjangoXBlockUserStateClient
from instructor_analytics.basic import list_problem_responses
from instructor_analytics.csvs import format_dictlist
from lms.djangoapps.certificates.models import GeneratedCertificate, CertificateStatuses, certificate_status
from lms.djangoapps.grades.context import grading_context, grading_context_for_course
from lms.djangoapps.grades.models import PersistentCourseGrade
from lms.djangoapps.grades.course_grade_factory import CourseGradeFactory
from lms.djangoapps.teams.models import CourseTeamMembership
from lms.djangoapps.verify_student.services import IDVerificationService
from openedx.core.djangoapps.content.block_structure.api import get_course_in_cache
from openedx.core.djangoapps.course_groups.cohorts import bulk_cache_cohorts, get_cohort, is_course_cohorted
from openedx.core.djangoapps.user_api.course_tag.api import BulkCourseTags
from smartlearn import format_course_duration
from student.models import CourseEnrollment, UserProfile
from student.roles import BulkRoleCache
from xmodule.modulestore.django import modulestore
from xmodule.partitions.partitions_service import PartitionService
from xmodule.split_test_module import get_split_user_partitions

from .runner import TaskProgress
from .utils import upload_csv_to_report_store

TASK_LOG = logging.getLogger('edx.celery.task')


def _flatten(iterable):
    return list(chain.from_iterable(iterable))


class _CourseCertificateReportContext(object):
    """
    Internal class that provides a common context to use for a single grade
    report.  When a report is parallelized across multiple processes,
    elements of this context are serialized and parsed across process
    boundaries.
    """
    def __init__(self, _xmodule_instance_args, _entry_id, course_id, _task_input, action_name):
        self.task_info_string = (
            u'Task: {task_id}, '
            u'InstructorTask ID: {entry_id}, '
            u'Course: {course_id}, '
            u'Input: {task_input}'
        ).format(
            task_id=_xmodule_instance_args.get('task_id') if _xmodule_instance_args is not None else None,
            entry_id=_entry_id,
            course_id=course_id,
            task_input=_task_input,
        )
        self.action_name = action_name
        self.course_id = course_id
        self.task_progress = TaskProgress(self.action_name, total=None, start_time=time())

    @lazy
    def course(self):
        return get_course_by_id(self.course_id)

    @lazy
    def course_structure(self):
        return get_course_in_cache(self.course_id)

    @lazy
    def course_experiments(self):
        return get_split_user_partitions(self.course.user_partitions)

    @lazy
    def teams_enabled(self):
        return self.course.teams_enabled

    @lazy
    def cohorts_enabled(self):
        return is_course_cohorted(self.course_id)

    @lazy
    def graded_assignments(self):
        """
        Returns an OrderedDict that maps an assignment type to a dict of
        subsection-headers and average-header.
        """
        grading_cxt = grading_context(self.course, self.course_structure)
        graded_assignments_map = OrderedDict()
        for assignment_type_name, subsection_infos in grading_cxt['all_graded_subsections_by_type'].iteritems():
            graded_subsections_map = OrderedDict()
            for subsection_index, subsection_info in enumerate(subsection_infos, start=1):
                subsection = subsection_info['subsection_block']
                header_name = u"{assignment_type} {subsection_index}: {subsection_name}".format(
                    assignment_type=assignment_type_name,
                    subsection_index=subsection_index,
                    subsection_name=subsection.display_name,
                )
                graded_subsections_map[subsection.location] = header_name

            average_header = u"{assignment_type}".format(assignment_type=assignment_type_name)

            # Use separate subsection and average columns only if
            # there's more than one subsection.
            separate_subsection_avg_headers = len(subsection_infos) > 1
            if separate_subsection_avg_headers:
                average_header += u" (Avg)"

            graded_assignments_map[assignment_type_name] = {
                'subsection_headers': graded_subsections_map,
                'average_header': average_header,
                'separate_subsection_avg_headers': separate_subsection_avg_headers,
                'grader': grading_cxt['subsection_type_graders'].get(assignment_type_name),
            }
        return graded_assignments_map

    def update_status(self, message):
        """
        Updates the status on the celery task to the given message.
        Also logs the update.
        """
        TASK_LOG.info(u'%s, Task type: %s, %s', self.task_info_string, self.action_name, message)
        return self.task_progress.update_task_state(extra_meta={'step': message})


class _CourseGradeBulkContext(object):
    def __init__(self, context, users):
        self.certs = _CertificateBulkContext(context, users)
        bulk_cache_cohorts(context.course_id, users)
        BulkRoleCache.prefetch(users)
        PersistentCourseGrade.prefetch(context.course_id, users)
        BulkCourseTags.prefetch(context.course_id, users)


class _CertificateBulkContext(object):
    def __init__(self, context, users):
        self.certificates_by_user = {
            certificate.user.id: certificate
            for certificate in
            GeneratedCertificate.objects.filter(course_id=context.course_id, user__in=users)
        }


class CourseCertificateReport(object):
    """
    Class to encapsulate functionality related to generating Grade Reports.
    """
    # Batch size for chunking the list of enrollees in the course.
    USER_BATCH_SIZE = 100

    @classmethod
    def generate(cls, _xmodule_instance_args, _entry_id, course_id, _task_input, action_name):
        """
        Public method to generate a grade report.
        """
        with modulestore().bulk_operations(course_id):
            context = _CourseCertificateReportContext(_xmodule_instance_args, _entry_id, course_id, _task_input, action_name)
            return CourseCertificateReport()._generate(context)

    def _generate(self, context):
        """
        Internal method for generating a grade report for the given context.
        """
        context.update_status(u'Starting certificate report')
        success_headers = self._success_headers(context)
        error_headers = self._error_headers()
        batched_rows = self._batched_rows(context)

        context.update_status(u'Compiling certificate report')
        success_rows, error_rows = self._compile(context, batched_rows)

        context.update_status(u'Uploading certificate report')
        self._upload(context, success_headers, success_rows, error_headers, error_rows)

        return context.update_status(u'Completed certificate report')

    def _success_headers(self, context):
        """
        Returns a list of all applicable column headers for this grade report.
        """
        return (
            ["Course Name", "Course Duration", "Certificate Mode", "Name", "Certificate ID", "Email", "Certificate Date"]
        )

    def _error_headers(self):
        """
        Returns a list of error headers for this grade report.
        """
        return ["Student ID", "Username", "Error"]

    def _batched_rows(self, context):
        """
        A generator of batches of (success_rows, error_rows) for this report.
        """
        for users in self._batch_users(context):
            users = filter(lambda u: u is not None, users)
            yield self._rows_for_users(context, users)

    def _compile(self, context, batched_rows):
        """
        Compiles and returns the complete list of (success_rows, error_rows) for
        the given batched_rows and context.
        """
        # partition and chain successes and errors
        success_rows, error_rows = izip(*batched_rows)
        success_rows = list(chain(*success_rows))
        error_rows = list(chain(*error_rows))

        # update metrics on task status
        context.task_progress.succeeded = len(success_rows)
        context.task_progress.failed = len(error_rows)
        context.task_progress.attempted = context.task_progress.succeeded + context.task_progress.failed
        context.task_progress.total = context.task_progress.attempted
        return success_rows, error_rows

    def _upload(self, context, success_headers, success_rows, error_headers, error_rows):
        """
        Creates and uploads a CSV for the given headers and rows.
        """
        date = datetime.now(UTC)
        upload_csv_to_report_store([success_headers] + success_rows, 'cert_report', context.course_id, date)
        if len(error_rows) > 0:
            error_rows = [error_headers] + error_rows
            upload_csv_to_report_store(error_rows, 'cert_report_err', context.course_id, date)

    def _batch_users(self, context):
        """
        Returns a generator of batches of users.
        """
        def grouper(iterable, chunk_size=self.USER_BATCH_SIZE, fillvalue=None):
            args = [iter(iterable)] * chunk_size
            return izip_longest(*args, fillvalue=fillvalue)

        def users_for_course(course_id):
            """
            Get all the enrolled users in a course.

            This method fetches & loads the enrolled user objects at once which may cause
            out-of-memory errors in large courses.
            """
            users = CourseEnrollment.objects.users_enrolled_in(course_id, include_inactive=True)
            users = users.select_related('profile')
            return grouper(users)

        task_log_message = u'{}, Task type: {}'.format(context.task_info_string, context.action_name)
        TASK_LOG.info(u'%s, Creating Course Certificate', task_log_message)
        batch_users = users_for_course(context.course_id)
        return batch_users

    def _user_certificate_info(self, user, context, course_grade, bulk_certs):
        """
        Returns the course certification information for the given user.
        """
        user_certificate = bulk_certs.certificates_by_user.get(user.id)
        status = certificate_status(user_certificate)
        certificate_generated = status['status'] == CertificateStatuses.downloadable

        if certificate_generated:
            certificate_date = user_certificate.created_date.strftime("%Y-%m-%d")
            certificate_id = user_certificate.verify_uuid
            certificate_mode = _(user_certificate.mode.title())

            return {
                'mode': certificate_mode,
                'id': certificate_id,
                'date': certificate_date
            }

        return None

    def _rows_for_users(self, context, users):
        """
        Returns a list of rows for the given users for this report.
        """
        with modulestore().bulk_operations(context.course_id):
            bulk_context = _CourseGradeBulkContext(context, users)

            success_rows, error_rows = [], []

            for user, course_grade, error in CourseGradeFactory().iter(
                users,
                course=context.course,
                collected_block_structure=context.course_structure,
                course_key=context.course_id,
            ):
                if not course_grade:
                    # An empty gradeset means we failed to grade a student.
                    error_rows.append([user.id, user.username, text_type(error)])
                else:
                    profile = UserProfile.objects.get(user=user)
                    cert_info = self._user_certificate_info(user, context, course_grade, bulk_context.certs)
                    if cert_info:
                        course_duration = format_course_duration(context.course) if context.course.start and context.course.end else ''
                        success_rows.append(
                            [context.course.display_name, course_duration, cert_info['mode']] +
                            [profile.name, cert_info['id'], user.email, cert_info['date']]
                        )
            return success_rows, error_rows
