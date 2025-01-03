from django.db import models
from django.conf import settings
from productos.models import Producto
from django.utils import timezone


class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    creado = models.DateTimeField(default=timezone.now)

    @property
    def total(self):
        """Calcula el total del carrito sumando los subtotales de las líneas."""
        return sum(linea.get_subtotal() for linea in self.lineas.all())

    def agregar_producto(self, producto, cantidad=1):
        """
        Agrega un producto al carrito o incrementa su cantidad.
        Si la línea no existe, la crea con el precio del producto actual.
        """
        if cantidad > producto.stock_disponible:
            raise ValueError("Cantidad supera el stock disponible.")

        linea, creada = self.lineas.get_or_create(
            producto=producto,
            defaults={'cantidad': cantidad, 'precio': producto.precio}
        )
        if not creada:
            # Incrementa la cantidad si ya existe
            linea.incrementar_cantidad(cantidad)
        # Verifica y actualiza el precio si ha cambiado
        if linea.precio != producto.precio:
            linea.precio = producto.precio
            linea.save()
        return linea

    def eliminar_producto(self, producto, cantidad=1):
        """
        Elimina una cantidad específica de un producto del carrito.
        Si la cantidad llega a 0, elimina la línea completa.
        """
        try:
            linea = self.lineas.get(producto=producto)
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


class LineaCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def incrementar_cantidad(self, cantidad=1):
        """Incrementa la cantidad de este producto en el carrito."""
        self.cantidad += cantidad
        self.save()

    def disminuir_cantidad(self, cantidad=1):
        """
        Disminuye la cantidad de este producto en el carrito.
        Si la cantidad llega a 0, elimina la línea.
        """
        self.cantidad -= cantidad
        if self.cantidad <= 0:
            self.delete()
        else:
            self.save()

    def get_subtotal(self):
        """Calcula el subtotal para esta línea."""
        return self.cantidad * self.precio

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Precio: ${self.precio})"
