from django.db import models
from pedidos.models import Pedido
from usuarios.models import Usuario

class HistorialCompra(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='historial_compras')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial_compras')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"HistorialCompra {self.id} - Pedido {self.pedido.id}"
