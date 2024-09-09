from django.contrib import admin
from .models import SiteConfiguration

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'maintenance_mode', 'support_email')
    search_fields = ('site_name', 'support_email')
    readonly_fields = ('site_name',)
