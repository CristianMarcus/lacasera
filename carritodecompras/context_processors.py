from carritodecompras.models import CarritoItem

def carrito_context(request):
    # Si el usuario no está autenticado, el carrito estará vacío
    if not request.user.is_authenticated:
        return {'total_items': 0, 'total_precio': 0}

    # Obtener los elementos del carrito del usuario autenticado
    carrito_items = CarritoItem.objects.filter(usuario=request.user)

    # Calcular el número total de productos en el carrito
    total_items = sum(item.cantidad for item in carrito_items)

    # Calcular el precio total del carrito
    total_precio = sum(item.producto.precio * item.cantidad for item in carrito_items)

    # Devolver los datos al contexto
    return {
        'total_items': total_items,
        'total_precio': total_precio
    }
