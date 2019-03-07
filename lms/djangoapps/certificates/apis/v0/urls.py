"""
Certificates API v0 URLs.
"""
from django.conf import settings
from django.conf.urls import include, url

from lms.djangoapps.certificates.apis.v0 import views

CERTIFICATES_URLS = ([
    url(
        r'^{username}/courses/{course_id}/$'.format(
            username=settings.USERNAME_PATTERN,
            course_id=settings.COURSE_ID_PATTERN
        ),
        views.CertificatesDetailView.as_view(),
        name='detail'
    ),
    url(
        r'^(?P<uuid>[0-9a-f]{32})$',
        views.CertificatesDetailViewByUUID.as_view(),
        name='cert_by_uuid'
    ),
], 'certificates')

app_name = 'v0'
urlpatterns = [
    url(r'^certificates/', include(CERTIFICATES_URLS)),
]
