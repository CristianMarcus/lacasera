from django.db import models

# Create your models here.
# Core - models.py
from django.db import models

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100)
    maintenance_mode = models.BooleanField(default=False)
    support_email = models.EmailField()

    def __str__(self):
        return self.site_name
