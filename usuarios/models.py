#from django.db import models
#
## Create your models here.
## Usuarios - models.py
#from django.contrib.auth.models import AbstractUser
#from django.db import models
#
#class Usuario(AbstractUser):
#    phone_number = models.CharField(max_length=15, blank=True, null=True)
#    address = models.CharField(max_length=255, blank=True, null=True)
#
#    def __str__(self):
#        return self.username
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Otros campos personalizados que desees agregar
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Cambia el related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',  # Cambia el related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

