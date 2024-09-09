from .models import Carrito

def carrito_total(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user).first()
        if carrito:
            return {'carrito_total': carrito.get_total()}
    return {'carrito_total': 0}
