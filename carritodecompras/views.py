# carritodecompras/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from productos.models import Producto
from .models import LineaCarrito
from .utils import obtener_carrito_usuario, actualizar_sesion_carrito

# VISTAS PARA USUARIOS AUTENTICADOS
@login_required
def ver_carrito(request):
    """
    Vista que muestra el carrito de compras para usuarios autenticados.
    Obtiene el carrito del usuario autenticado y lista los productos dentro de él,
    calculando el total de artículos y el total de precio.
    """
    carrito = obtener_carrito_usuario(request)
    lineas = LineaCarrito.objects.filter(carrito=carrito)
    
    total_items = sum(linea.cantidad for linea in lineas)
    total_precio = sum(linea.producto.precio * linea.cantidad for linea in lineas)

    return render(request, 'carritodecompras/ver_carrito.html', {
        'lineas': lineas,
        'total_items': total_items,
        'total_precio': total_precio
    })

@login_required
def agregar_al_carrito(request, producto_id):
    """
    Vista que agrega un producto al carrito para usuarios autenticados.
    Si el producto ya existe en el carrito, aumenta la cantidad. Si no existe, lo agrega con cantidad 1.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = obtener_carrito_usuario(request)
    
    # Obtiene la línea del carrito o la crea si no existe
    linea, created = LineaCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    
    # Solo aumenta la cantidad si la línea ya existía
    if not created:
        linea.cantidad += 1
    
    linea.save()

    messages.success(request, f'{producto.nombre} fue agregado al carrito.')
    return redirect('ver_carrito')


@login_required
def eliminar_producto(request, producto_id):
    """
    Vista que elimina un producto del carrito para usuarios autenticados.
    Si el producto tiene más de una unidad en el carrito, disminuye la cantidad.
    Si solo queda una unidad, la elimina completamente.
    """
    carrito = obtener_carrito_usuario(request)
    linea = get_object_or_404(LineaCarrito, carrito=carrito, producto_id=producto_id)

    if linea.cantidad > 1:
        linea.cantidad -= 1
        linea.save()
    else:
        linea.delete()

    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('ver_carrito')


# VISTAS PARA USUARIOS NO AUTENTICADOS (CARRO EN SESIÓN)
def ver_carrito_sesion(request):
    """
    Vista que muestra el carrito de compras para usuarios no autenticados.
    El carrito se maneja dentro de la sesión del usuario.
    """
    carrito = request.session.get('carrito', {})
    total_carrito = sum(item['total_precio'] for item in carrito.values())

    return render(request, 'carritodecompras/ver_carrito_sesion.html', {
        'carrito': carrito,
        'total_carrito': total_carrito
    })

def agregar_producto_sesion(request, producto_id):
    """
    Vista que agrega un producto al carrito para usuarios no autenticados.
    El carrito se guarda en la sesión del usuario.
    """
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 0))
    
    if cantidad <= 0:
        messages.error(request, "La cantidad debe ser mayor que cero.")
        return redirect('ver_carrito_sesion')

    # Asegúrate de manejar la situación donde el producto ya existe en la sesión
    carrito = actualizar_sesion_carrito(request, producto, cantidad)
    messages.success(request, f"{producto.nombre} fue agregado al carrito.")
    return redirect('ver_carrito_sesion')

def eliminar_producto_sesion(request, producto_id):
    """
    Vista que elimina un producto del carrito para usuarios no autenticados.
    El carrito se maneja en la sesión, y si el producto tiene más de una unidad, disminuye la cantidad;
    si solo queda una unidad, lo elimina completamente del carrito en la sesión.
    """
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)

    if producto_id in carrito:
        if carrito[producto_id]['cantidad'] > 1:
            carrito[producto_id]['cantidad'] -= 1
            carrito[producto_id]['total_precio'] = float(carrito[producto_id]['precio']) * carrito[producto_id]['cantidad']
        else:
            del carrito[producto_id]

        request.session['carrito'] = carrito
        messages.success(request, 'Producto eliminado del carrito.')

    return redirect('ver_carrito_sesion')
