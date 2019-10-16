# -*- coding: utf-8 -*-
"""
Contains code related to computing content gating course duration limits
and course access based on these limits.
"""
from datetime import timedelta

from django.apps import apps
from django.utils import timezone
from django.utils.translation import ugettext as _

from course_modes.models import CourseMode
from util.date_utils import DEFAULT_SHORT_DATE_FORMAT, strftime_localized
from lms.djangoapps.courseware.access_response import AccessError
from lms.djangoapps.courseware.access_utils import ACCESS_GRANTED
from lms.djangoapps.courseware.date_summary import verified_upgrade_deadline_link
from openedx.core.djangoapps.catalog.utils import get_course_run_details
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from openedx.core.djangoapps.util.user_messages import PageLevelMessages
from openedx.core.djangolib.markup import HTML
from openedx.features.course_duration_limits.models import CourseDurationLimitConfig
from student.roles import CourseBetaTesterRole

MIN_DURATION = timedelta(weeks=4)
MAX_DURATION = timedelta(weeks=12)


class AuditExpiredError(AccessError):
    """
    Access denied because the user's audit timespan has expired
    """
    def __init__(self, user, course, expiration_date):
        error_code = "audit_expired"
        developer_message = "User {} had access to {} until {}".format(user, course, expiration_date)
        expiration_date = strftime_localized(expiration_date, DEFAULT_SHORT_DATE_FORMAT)
        user_message = _("Access expired on {expiration_date}").format(expiration_date=expiration_date)
        try:
            course_name = CourseOverview.get_from_id(course.id).display_name_with_default
            additional_context_user_message = _("Access to {course_name} expired on {expiration_date}").format(
                course_name=course_name,
                expiration_date=expiration_date
            )
        except CourseOverview.DoesNotExist:
            additional_context_user_message = _("Access to the course you were looking"
                                                "for expired on {expiration_date}").format(
                expiration_date=expiration_date
            )
        super(AuditExpiredError, self).__init__(error_code, developer_message, user_message,
                                                additional_context_user_message)


def get_user_course_expiration_date(user, course):
    """
    Return expiration date for given user course pair.
    Return None if the course does not expire.

    Business Logic:
      - Course access duration is bounded by the min and max duration.
      - If course fields are missing, default course access duration to MIN_DURATION.
    """

    if not CourseMode.verified_mode_for_course(course.id):
        return None

    CourseEnrollment = apps.get_model('student.CourseEnrollment')
    enrollment = CourseEnrollment.get_enrollment(user, course.id)
    if enrollment is None or enrollment.mode != 'audit' or course.end is None:
        return None

    # if the user is a beta tester their access should not expire
    if CourseBetaTesterRole(course.id).has_user(user):
        return None

    # course.end + 1 week
    return course.end + timedelta(weeks=1)


def check_course_expired(user, course):
    """
    Check if the course expired for the user.
    """
    if not CourseDurationLimitConfig.enabled_for_enrollment(user=user, course_key=course.id):
        return ACCESS_GRANTED

    expiration_date = get_user_course_expiration_date(user, course)
    if expiration_date and timezone.now() > expiration_date:
        return AuditExpiredError(user, course, expiration_date)

    return ACCESS_GRANTED


def register_course_expired_message(request, course):
    """
    Add a banner notifying the user of the user course expiration date if it exists.
    """
    if CourseDurationLimitConfig.enabled_for_enrollment(user=request.user, course_key=course.id):
        expiration_date = get_user_course_expiration_date(request.user, course)
        if expiration_date:
            upgrade_message = _('Your access to this course expires on {expiration_date}. \
                    <a href="{upgrade_link}">Upgrade now</a> for unlimited access.')
            PageLevelMessages.register_info_message(
                request,
                HTML(upgrade_message).format(
                    expiration_date=expiration_date.strftime('%b %-d'),
                    upgrade_link=verified_upgrade_deadline_link(user=request.user, course=course)
                )
            )
