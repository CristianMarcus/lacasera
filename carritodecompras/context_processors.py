# carritodecompras/context_processors.py

from django.contrib.auth.models import AnonymousUser
from .models import Carrito  # Asegúrate de que este es el modelo correcto
from .models import CarritoItem  # Asegúrate de que este modelo esté definido

def carrito_context(request):
    carrito_items = []  # Inicializamos carrito_items como una lista vacía
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            carrito_items = carrito.carritoitem_set.all()  # Obtener los items del carrito
        except Carrito.DoesNotExist:
            carrito_items = []  # Si no existe el carrito, aseguramos que esté vacío
    return {
        'carrito_items': carrito_items,
    }
