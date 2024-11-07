# pedidos/models.py

from django.db import models
from carritodecompras.models import Producto
from django.conf import settings

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos_pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=[
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
        ('Cancelado', 'Cancelado'),
    ], default='Pendiente')

    def __str__(self):
        return f"Pedido {self.id} de {self.usuario.username}"

class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='lineas_pedido_pedidos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lineas_pedido_pedidos')
    cantidad = models.IntegerField()

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")
        if not self.producto.disponible:
            raise ValidationError("El producto no está disponible.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
