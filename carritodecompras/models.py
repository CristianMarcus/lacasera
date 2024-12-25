from django.db import models
from django.conf import settings
from productos.models import Producto, VariedadEmpanada
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
    carrito = models.ForeignKey(Carrito, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variedad = models.ForeignKey(VariedadEmpanada, on_delete=models.CASCADE)  # Añade este campo
    cantidad = models.IntegerField(default=1)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def incrementar_cantidad(self, cantidad=1):
        self.cantidad += cantidad
        self.save()

    def disminuir_cantidad(self, cantidad=1):
        self.cantidad -= cantidad
        if self.cantidad < 1:
            self.delete()
        else:
            self.save()

    def get_subtotal(self):
        return self.cantidad * self.precio_unidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} ({self.variedad.nombre_variedad})"

