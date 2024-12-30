from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Solo un precio general
    descripcion = models.TextField()
    disponible = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    imagen = models.ImageField(upload_to='static/productos', blank=True, null=True)

    def __str__(self):
        return self.nombre


    def get_precio(self, cantidad):
        """Devuelve el precio según la cantidad para empanadas."""
        if self.es_empanada:
            if cantidad >= 12:
                return self.precio_docena or self.precio_unidad
            elif cantidad >= 6:
                return self.precio_media_docena or self.precio_unidad
        return self.precio_unidad
        

