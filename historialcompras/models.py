from django.db import models

# Create your models here.
# HistorialCompras - models.py
from django.db import models
from usuarios.models import Usuario
from pedidos.models import Pedido

class HistorialCompra(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Historial de {self.usuario.username}"
