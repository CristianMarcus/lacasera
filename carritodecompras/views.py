from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from productos.models import Producto, VariedadEmpanada
from .models import LineaCarrito, Carrito
from .forms import PedidoContactoForm, AgregarCarritoForm
from pedidos.models import Pedido
from .utils import obtener_carrito_usuario, actualizar_sesion_carrito

@login_required
def ver_carrito(request):
    # Obtener o crear el carrito asociado al usuario
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Seleccionar líneas del carrito
    lineas = carrito.lineas.select_related('producto').all()

    # Calcular totales
    total_items = sum(linea.cantidad for linea in lineas)
    total_precio = sum(linea.get_subtotal() for linea in lineas)

    # Obtener o crear el pedido en estado "Pendiente"
    pedido, created = Pedido.objects.get_or_create(
        cliente=request.user,
        estado="Pendiente",
        defaults={'total': total_precio}
    )

    # Si el pedido ya existía, actualizar el total
    if not created:
        pedido.total = total_precio
        pedido.save()

    # Preparar el formulario de contacto
    form = PedidoContactoForm(initial={
        'direccion': pedido.direccion or '',
        'telefono': pedido.telefono or '',
    })

    return render(request, 'carritodecompras/ver_carrito.html', {
        'carrito': carrito,
        'lineas': lineas,
        'total_items': total_items,
        'total_precio': total_precio,
        'form': form,
        'pedido': pedido,  # Asegúrate de pasar 'pedido' al contexto
    })




@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad <= 0:
        messages.error(request, "La cantidad debe ser un número positivo.")
        return redirect('productos:menu')

    linea, created = LineaCarrito.objects.get_or_create(
        carrito=carrito, producto=producto,
        defaults={'cantidad': cantidad, 'precio_unidad': producto.precio_unidad}
    )

    if not created:
        linea.cantidad += cantidad
        linea.save()

    messages.success(request, f"Agregaste {cantidad} unidades de {producto.nombre} al carrito.")
    return redirect('carritodecompras:ver_carrito')

@login_required
def eliminar_producto(request, producto_id):
    carrito = obtener_carrito_usuario(request)
    linea = get_object_or_404(LineaCarrito, carrito=carrito, producto_id=producto_id)

    linea.delete()
    messages.success(request, f"{linea.producto.nombre} ha sido eliminado del carrito.")
    return redirect('carritodecompras:ver_carrito')

@login_required
def disminuir_cantidad_producto(request, producto_id):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    linea = get_object_or_404(LineaCarrito, carrito=carrito, producto_id=producto_id)
    if linea.cantidad > 1:
        linea.cantidad -= 1
        linea.save()
    else:
        linea.delete()
    return redirect('carritodecompras:ver_carrito')

@login_required
def incrementar_cantidad_producto(request, producto_id):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    linea = get_object_or_404(LineaCarrito, carrito=carrito, producto_id=producto_id)
    linea.cantidad += 1
    linea.save()
    return redirect('carritodecompras:ver_carrito')

def ver_carrito_sesion(request):
    carrito = request.session.get('carrito', {})
    total_carrito = sum(item['cantidad'] * item['precio'] for item in carrito.values())

    return render(request, 'carritodecompras/ver_carrito_sesion.html', {
        'carrito': carrito,
        'total_carrito': total_carrito
    })

def agregar_producto_sesion(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad <= 0:
        messages.error(request, "La cantidad debe ser mayor que cero.")
        return redirect('carritodecompras:ver_carrito_sesion')

    carrito = actualizar_sesion_carrito(request, producto, cantidad)
    messages.success(request, f"{producto.nombre} fue agregado al carrito.")
    return redirect('carritodecompras:ver_carrito_sesion')

def eliminar_producto_sesion(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)

    if producto_id in carrito:
        if carrito[producto_id]['cantidad'] > 1:
            carrito[producto_id]['cantidad'] -= 1
            carrito[producto_id]['total_precio'] = carrito[producto_id]['cantidad'] * carrito[producto_id]['precio']
        else:
            del carrito[producto_id]

    request.session['carrito'] = carrito
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carritodecompras:ver_carrito_sesion')

@login_required
def procesar_pago_stripe(request):
    return render(request, 'carritodecompras/procesar_pago_stripe.html')

@login_required
def procesar_pago_mp(request):
    return render(request, 'carritodecompras/procesar_pago_mp.html')

@login_required
def actualizar_contacto_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        form = PedidoContactoForm(request.POST)
        if form.is_valid():
            pedido.direccion = form.cleaned_data['direccion']
            pedido.telefono = form.cleaned_data['telefono']
            pedido.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})

    form = PedidoContactoForm(initial={
        'direccion': pedido.direccion,
        'telefono': pedido.telefono,
    })

    return render(request, 'carritodecompras/actualizar_contacto_pedido.html', {'form': form, 'pedido': pedido})

@login_required
def confirmar_pago(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    lineas = carrito.lineas.all()

    if not lineas:
        messages.error(request, "Tu carrito está vacío. No puedes confirmar el pago.")
        return redirect('carritodecompras:ver_carrito')

    total_precio = sum(linea.get_subtotal() for linea in lineas)

    pedido, created = Pedido.objects.get_or_create(
        cliente=request.user,
        estado="Pendiente",
        defaults={'total': total_precio}
    )

    if not created:
        pedido.total = total_precio
        pedido.save()

    pedido.estado = "Confirmado"
    pedido.save()

    carrito.lineas.all().delete()
    messages.success(request, "Pedido confirmado exitosamente. ¡Gracias por tu compra!")

    return redirect('historialcompras:ver_historial')
