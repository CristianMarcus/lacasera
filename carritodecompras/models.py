from django.db import models
from django.conf import settings
from productos.models import Producto, VariedadEmpanada  # Asegúrate de tener estos modelos
from django.utils import timezone

# Modelo para el carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(default=timezone.now)

    def get_total(self):
        """Calcula el total del carrito."""
        return sum(linea.get_subtotal() for linea in self.lineas.all())

    def __str__(self):
        return f"Carrito {self.id} de {self.usuario.username}"

# Modelo para las líneas del carrito
class LineaCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variedad = models.ForeignKey(
        VariedadEmpanada, null=True, blank=True, on_delete=models.CASCADE
    )  # Opcional, en caso de productos con variedades
    cantidad = models.IntegerField(default=1)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def incrementar_cantidad(self, cantidad=1):
        """Incrementa la cantidad de este producto en el carrito."""
        self.cantidad += cantidad
        self.save()

    def disminuir_cantidad(self, cantidad=1):
        """Disminuye la cantidad o elimina la línea si llega a 0."""
        self.cantidad -= cantidad
        if self.cantidad < 1:
            self.delete()
        else:
            self.save()

    def get_subtotal(self):
        """Calcula el subtotal para esta línea."""
        return self.cantidad * self.precio_unidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
