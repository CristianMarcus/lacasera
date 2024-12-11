from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from productos.models import Producto
from .models import LineaCarrito, Carrito
from .utils import obtener_carrito_usuario, actualizar_sesion_carrito

from django.contrib.messages import get_messages

@login_required
def ver_carrito(request):
    carrito = obtener_carrito_usuario(request)
    lineas = LineaCarrito.objects.filter(carrito=carrito).select_related('producto')
    
    total_items = sum(linea.cantidad for linea in lineas if linea.producto)
    total_precio = sum(linea.get_subtotal() for linea in lineas if linea.producto)
    
    mensajes = get_messages(request)

    return render(request, 'carritodecompras/ver_carrito.html', {
        'lineas': lineas,
        'total_items': total_items,
        'total_precio': total_precio,
        'mensajes': mensajes
    })



@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = obtener_carrito_usuario(request)
    linea, created = LineaCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    
    if not created:
        linea.cantidad += 1
    
    linea.save()
    messages.success(request, f'{producto.nombre} fue agregado al carrito.')
    return redirect('carrito')

@login_required
def eliminar_producto(request, producto_id):
    carrito = obtener_carrito_usuario(request)
    
    try:
        linea = get_object_or_404(LineaCarrito, carrito=carrito, producto_id=producto_id)
    except:
        messages.error(request, 'El producto no se encuentra en tu carrito.')
        return redirect('carrito')
    
    if linea.cantidad > 1:
        linea.cantidad -= 1
        linea.save()
    else:
        linea.delete()
    
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito')

# Vistas para usuarios no autenticados (carro en sesión)

def ver_carrito_sesion(request):
    carrito = request.session.get('carrito', {})
    total_carrito = sum(item['total_precio'] for item in carrito.values())

    return render(request, 'carritodecompras/ver_carrito_sesion.html', {
        'carrito': carrito,
        'total_carrito': total_carrito
    })





def agregar_producto_sesion(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 0))
    
    if cantidad <= 0:
        messages.error(request, "La cantidad debe ser mayor que cero.")
        return redirect('ver_carrito_sesion')
    
    carrito = actualizar_sesion_carrito(request, producto, cantidad)
    messages.success(request, f"{producto.nombre} fue agregado al carrito.")
    return redirect('ver_carrito_sesion')

def eliminar_producto_sesion(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)
    
    if producto_id in carrito:
        if carrito[producto_id]['cantidad'] > 1:
            carrito[producto_id]['cantidad'] -= 1
            carrito[producto_id]['total_precio'] = float(carrito[producto_id]['precio']) * carrito[producto_id]['cantidad']
        else:
            del carrito[producto_id]  # Eliminar producto cuando la cantidad llega a cero
    
    request.session['carrito'] = carrito  # Actualizar el carrito en la sesión
    messages.success(request, 'Producto eliminado del carrito.')
    print("Carrito después de eliminar:", carrito)  # Debugging
    return redirect('ver_carrito_sesion')



# Vistas para procesar pagos con Stripe y Mercado Pago

@login_required
def procesar_pago_stripe(request):
    # Lógica para procesar el pago con Stripe
    return render(request, 'carritodecompras/procesar_pago_stripe.html')

@login_required
def procesar_pago_mp(request):
    # Lógica para procesar el pago con Mercado Pago
    return render(request, 'carritodecompras/procesar_pago_mp.html')
