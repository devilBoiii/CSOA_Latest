from django.contrib import admin
from .models import *
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'email', 'role', 'organization')
    search_fields = ('full_name', 'username', 'email')

class CertificateApplicationsAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'application_date', 'uploader_cso_name', 'status')
    search_fields = ('application_id', 'uploader_cso_name')
    
admin.site.register(users)
admin.site.register(SignInDetails)
admin.site.register(user_roles)
admin.site.register(organizations)
admin.site.register(system_process)
admin.site.register(gewog)
admin.site.register(dzongkhags)
admin.site.register(cso_types)
admin.site.register(thematic_area)
admin.site.register(profile_attachments)
admin.site.register(cso_closing_type)
admin.site.register(certificate_application)
admin.site.register(CSO_lists)
admin.site.register(post_publish)
