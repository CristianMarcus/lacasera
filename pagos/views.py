# pagos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pedido, LineaPedido
from .forms import CheckoutForm
from carritodecompras.models import Carrito, LineaCarrito
from django.conf import settings

@login_required
def checkout(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    
    if not carrito:
        return redirect('carrito')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Recoger datos del formulario
            nombre = form.cleaned_data['nombre']
            direccion = form.cleaned_data['direccion']
            ciudad = form.cleaned_data['ciudad']
            telefono = form.cleaned_data['telefono']
            
            # Crear pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                nombre=nombre,
                direccion=direccion,
                ciudad=ciudad,
                telefono=telefono,
                total=carrito.get_total(),  # Implementar get_total en el modelo Carrito
            )
            
            # Crear líneas de pedido
            lineas_carrito = LineaCarrito.objects.filter(carrito=carrito)
            for linea in lineas_carrito:
                LineaPedido.objects.create(
                    pedido=pedido,
                    producto=linea.producto,
                    cantidad=linea.cantidad,
                    precio=linea.precio,
                )
            
            # Vaciar carrito después del pedido
            carrito.delete()
            
            # Redirigir al usuario a la página de éxito
            return redirect('checkout_success')
    
    else:
        form = CheckoutForm()
    
    return render(request, 'pagos/checkout.html', {'form': form})
