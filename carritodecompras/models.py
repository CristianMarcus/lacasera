from django.db import models
from productos.models import Producto
from usuarios.models import Usuario

from django.db import models
from usuarios.models import Usuario
from productos.models import Producto

from django.utils import timezone

class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)  # Cambia auto_now_add por default2

    def __str__(self):
        return f'Carrito de {self.usuario}'

class LineaCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'


class CarritoItem(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.producto.nombre} - {self.cantidad} unidades'
