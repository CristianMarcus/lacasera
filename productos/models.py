from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio_docena = models.DecimalField(max_digits=10, decimal_places=2, default=14000)
    precio_media_docena = models.DecimalField(max_digits=10, decimal_places=2, default=8000)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disponible = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    imagen = models.ImageField(upload_to='static/productos', blank=True, null=True)
    es_empanada = models.BooleanField(default=False)  # Campo para identificar empanadas

    def __str__(self):
        return self.nombre

class VariedadEmpanada(models.Model):
    producto = models.ForeignKey(Producto, related_name='variedades', on_delete=models.CASCADE)
    nombre_variedad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre_variedad} - {self.producto.nombre}"
