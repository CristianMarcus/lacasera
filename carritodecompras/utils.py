# carritodecompras/utils.py

from .models import Carrito

def obtener_carrito_usuario(request):
    """
    Devuelve el carrito del usuario autenticado. Si no existe, lo crea.
    """
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        return carrito
    else:
        return None


def actualizar_sesion_carrito(request, producto, cantidad):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto.id)
    
    if producto_id in carrito:
        carrito[producto_id]['cantidad'] += cantidad
        carrito[producto_id]['total_precio'] = float(carrito[producto_id]['precio']) * carrito[producto_id]['cantidad']
    else:
        carrito[producto_id] = {
            'nombre': producto.nombre,
            'precio': str(producto.precio),
            'cantidad': cantidad,
            'total_precio': float(producto.precio) * cantidad
        }
    
    request.session['carrito'] = carrito
    return carrito
