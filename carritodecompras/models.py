from django.db import models
from django.conf import settings
from productos.models import Producto, VariedadEmpanada
from django.utils import timezone


# Modelo para el carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(default=timezone.now)

    @property
    def total(self):
        """Calcula el total del carrito sumando los subtotales de las líneas."""
        return sum(linea.get_subtotal() for linea in self.lineas.all())

    def agregar_producto(self, producto, cantidad=1, variedad=None):
        """Agrega un producto al carrito o incrementa su cantidad."""
        linea, creada = self.lineas.get_or_create(producto=producto, variedad=variedad)
        if creada:
            # Asegurarse de asignar el precio del producto actual
            linea.precio_unidad = producto.precio_unidad
        else:
            linea.incrementar_cantidad(cantidad)
        linea.save()
        return linea

    def eliminar_producto(self, producto, cantidad=1, variedad=None):
        """Elimina una cantidad específica de un producto del carrito o elimina la línea completa si la cantidad llega a 0."""
        try:
            linea = self.lineas.get(producto=producto, variedad=variedad)
            if cantidad >= linea.cantidad:
                linea.delete()
            else:
                linea.disminuir_cantidad(cantidad)
        except LineaCarrito.DoesNotExist:
            pass

    def vaciar_carrito(self):
        """Elimina todas las líneas del carrito."""
        self.lineas.all().delete()

    def __str__(self):
        return f"Carrito {self.id} de {self.usuario.username}"


# Modelo para las líneas del carrito
class LineaCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    variedad = models.ForeignKey(
        VariedadEmpanada, null=True, blank=True, on_delete=models.CASCADE
    )  # Opcional, en caso de productos con variedades
    cantidad = models.PositiveIntegerField(default=1)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def incrementar_cantidad(self, cantidad=1):
        """Incrementa la cantidad de este producto en el carrito."""
        self.cantidad += cantidad
        self.save()

    def disminuir_cantidad(self, cantidad=1):
        """Disminuye la cantidad o elimina la línea si llega a 0."""
        self.cantidad -= cantidad
        if self.cantidad <= 0:
            self.delete()
        else:
            self.save()

    def get_subtotal(self):
        """Calcula el subtotal para esta línea."""
        return self.cantidad * self.precio_unidad

    def save(self, *args, **kwargs):
        """Asegura que el precio por unidad esté siempre sincronizado con el precio del producto."""
        if self.precio_unidad != self.producto.precio_unidad:
            self.precio_unidad = self.producto.precio_unidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
