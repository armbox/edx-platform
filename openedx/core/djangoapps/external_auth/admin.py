'''
django admin pages for courseware model
'''

from django.contrib import admin

from openedx.core.djangoapps.external_auth.models import ExternalAuthMap, EnrollEmailDomainMap


class ExternalAuthMapAdmin(admin.ModelAdmin):
    """
    Admin model for ExternalAuthMap
    """
    search_fields = ['external_id', 'user__username']
    date_hierarchy = 'dtcreated'


class EnrollEmailDomainMapAdmin(admin.ModelAdmin):
    """
    Admin model for EnrollDomainMap
    """
    list_display = ('external_id', 'domain', 'disallow',)
    search_fields = ['external_id', 'domain']


admin.site.register(ExternalAuthMap, ExternalAuthMapAdmin)
admin.site.register(EnrollEmailDomainMap, EnrollEmailDomainMapAdmin)
