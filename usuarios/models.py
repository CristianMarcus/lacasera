from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    phone_number = models.CharField('Número de teléfono', max_length=15, blank=True)
    address = models.CharField('Dirección', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'
