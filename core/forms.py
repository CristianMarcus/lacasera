from django import forms
from .models import SiteConfiguration

class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = ['site_name', 'maintenance_mode', 'support_email']
