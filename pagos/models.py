from django.db import models
from pedidos.models import Pedido

class Pago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pago {self.id} - Pedido {self.pedido.id}"
