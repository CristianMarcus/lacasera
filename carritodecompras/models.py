from django.db import models
from django.conf import settings
from productos.models import Producto
from django.utils import timezone

class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    creado = models.DateTimeField(default=timezone.now)

    def get_total(self):
        total = sum(linea.get_subtotal() for linea in self.lineas.all())
        return total

    def __str__(self):
        return f"Carrito {self.id} de {self.usuario.username}"

class LineaCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='lineas', on_delete=models.CASCADE, default=1)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, default=1)
    cantidad = models.IntegerField(default=1)  # Asegurarse de que el campo cantidad tenga un valor predeterminado

    def get_subtotal(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
