from django.db import models
from productos.models import Producto
from django.utils.timezone import now

class Pedido(models.Model):
    cliente = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    estado = models.CharField(max_length=50)  # Aquí debe ser `max_length`
    fecha_pedido = models.DateTimeField(default=now)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    direccion = models.CharField(max_length=255, blank=True, null=True) 
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.username}"

class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="lineas", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Clave foránea a Producto
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
