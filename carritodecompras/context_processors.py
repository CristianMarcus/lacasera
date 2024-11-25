# carritodecompras/context_processors.py

from .models import Carrito, LineaCarrito

def carrito_context(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if carrito:
            lineas = LineaCarrito.objects.filter(carrito=carrito).select_related('producto')
            total_items = sum(linea.cantidad for linea in lineas if linea.producto)
            total_precio = sum(linea.get_subtotal() for linea in lineas if linea.producto)
        else:
            total_items = 0
            total_precio = 0
    else:
        carrito = request.session.get('carrito', {})
        total_items = sum(item['cantidad'] for item in carrito.values())
        total_precio = sum(item['total_precio'] for item in carrito.values())

    return {
        'total_items': total_items,
        'total_precio': total_precio
    }
