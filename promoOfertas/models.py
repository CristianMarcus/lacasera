from django.db import models

# Create your models here.
# Promociones - models.py
from django.db import models
from productos.models import Producto
from django.core.exceptions import ValidationError

class Promocion(models.Model):
    nombre = models.CharField(max_length=100)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    productos = models.ManyToManyField(Producto)

    def __str__(self):
        return self.nombre
    
    def clean(self):
        # Validar que la fecha de inicio no sea posterior a la de fin
        if self.fecha_inicio > self.fecha_fin:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")

    def save(self, *args, **kwargs):
        # Llamamos a clean() antes de guardar el modelo
        self.clean()
        super(Promocion, self).save(*args, **kwargs)