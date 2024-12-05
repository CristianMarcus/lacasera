# carritodecompras/models.py

from django.db import models
from productos.models import Producto
from usuarios.models import Usuario
from django.utils import timezone


class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def get_total(self):
        total = sum(linea.get_subtotal() for linea in self.lineacarrito_set.all())
        return total

    def __str__(self):
        return f'Carrito de {self.usuario}'

class LineaCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.SET_NULL, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=1)

    def get_subtotal(self):
        if self.producto:
            return self.cantidad * self.producto.precio
        return 0  # Devuelve 0 si el producto es None

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre if self.producto else "Producto eliminado"}'
