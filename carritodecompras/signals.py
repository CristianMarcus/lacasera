# carritodecompras/signals.py

from django.db.models.signals import post_delete
from django.dispatch import receiver
from productos.models import Producto
from .models import LineaCarrito

@receiver(post_delete, sender=Producto)
def eliminar_lineas_carrito(sender, instance, **kwargs):
    LineaCarrito.objects.filter(producto=instance).delete()
