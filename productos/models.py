from django.db import models





class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)  # Campo stock agregado
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    imagen = models.ImageField(upload_to='static/productos', blank=True, null=True)

    def __str__(self):
        return self.nombre
