from django.db import models

# Create your models here.
# Productos - models.py
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)  # Para manejar stock
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Para manejar imágenes

    def __str__(self):
        return self.nombre
