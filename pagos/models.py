# pagos/models.py
from django.db import models

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=100)
    # Otros campos...

class Transaccion(models.Model):
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    # Otros campos...

class Pedido(models.Model):
    # Campos del modelo Pedido
    pass

class LineaPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    # Otros campos...
