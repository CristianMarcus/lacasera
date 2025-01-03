from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from productos.models import Producto
from .models import LineaCarrito, Carrito
from .forms import PedidoContactoForm, AgregarCarritoForm
from pedidos.models import Pedido, LineaPedido
from .utils import obtener_carrito_usuario, actualizar_sesion_carrito
from django.core.exceptions import PermissionDenied

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

    # Verificar si hay datos en la sesión para dirección y teléfono
    direccion = request.session.get('direccion', pedido.direccion)
    telefono = request.session.get('telefono', pedido.telefono)

    # Imprimir los datos de la sesión
    print("Dirección de la sesión:", direccion)
    print("Teléfono de la sesión:", telefono)

    # Preparar el formulario de contacto
    form = PedidoContactoForm(initial={
        'direccion': direccion,
        'telefono': telefono,
    })

    return render(request, 'carritodecompras/ver_carrito.html', {
        'carrito': carrito,
        'lineas': lineas,
        'total_items': total_items,
        'total_precio': total_precio,
        'form': form,
        'pedido': pedido,  # Agregado al contexto
    })


    return render(request, 'carritodecompras/ver_carrito.html', {
        'carrito': carrito,
        'lineas': lineas,
        'total_items': total_items,
        'total_precio': total_precio,
        'form': form,
        'pedido': pedido,  # Agregado al contexto
    })


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser mayor que cero.")
            return redirect('productos:detalle_producto', producto_id=producto.id)

        # Agregar o actualizar el producto en el carrito
        linea, created = LineaCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad, 'precio': producto.precio}
        )

        if not created:
            # Incrementar cantidad si la línea ya existía
            linea.incrementar_cantidad(cantidad)
        linea.save()

        messages.success(request, f"{producto.nombre} ha sido agregado al carrito.")
        return redirect('carritodecompras:ver_carrito')

    return redirect('productos:detalle_producto', producto_id=producto.id)



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
def actualizar_contacto(request, pedido_id):
    # Obtén el pedido correspondiente
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        form = PedidoContactoForm(request.POST)
        if form.is_valid():
            # Solo actualizamos la sesión, no la base de datos
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']
            
            # Guardamos los datos actualizados en la sesión
            request.session['direccion'] = direccion
            request.session['telefono'] = telefono

            messages.success(request, "El contacto se actualizó correctamente en la sesión.")
            
            # Imprimir los datos que realmente se están guardando en la sesión
            print("Dirección guardada en la sesión:", request.session.get('direccion'))
            print("Teléfono guardado en la sesión:", request.session.get('telefono'))
            
            return redirect('carritodecompras:ver_carrito')  # Redirigimos al carrito

        else:
            print(form.errors)  # Muestra los errores en consola para depuración
    else:
        initial_data = {
            'direccion': request.session.get('direccion', pedido.direccion or ''),
            'telefono': request.session.get('telefono', pedido.telefono or ''),
        }
        form = PedidoContactoForm(initial=initial_data)

    return render(request, 'carritodecompras/actualizar_contacto.html', {'form': form, 'pedido': pedido})


@login_required
def confirmar_pago(request):
    # Obtener o crear el carrito del usuario actual
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    lineas = carrito.lineas.all()

    # Verificar si el carrito está vacío
    if not lineas:
        messages.error(request, "Tu carrito está vacío. No puedes confirmar el pago.")
        return redirect('carritodecompras:ver_carrito')

    # Calcular el precio total del carrito
    total_precio = sum(linea.get_subtotal() for linea in lineas)

    # Obtener o crear un pedido en estado "Pendiente" para el usuario actual
    pedido, created = Pedido.objects.get_or_create(
        cliente=request.user,
        estado="Pendiente",
        defaults={'total': total_precio}
    )

    if not created:
        # Si el pedido ya existía, actualizar el total
        pedido.total = total_precio

    # Cambiar el estado del pedido a "Confirmado"
    pedido.estado = "Confirmado"

    # Usar los datos de la sesión si existen
    # Primero asignamos la dirección de la sesión, si existe
    if 'direccion' in request.session:
        pedido.direccion = request.session['direccion']
    else:
    # Si no está en la sesión, usamos la dirección de la base de datos
        pedido.direccion = pedido.cliente.address

# Luego, asignamos el teléfono de la sesión, si existe
    if 'telefono' in request.session:
        pedido.telefono = request.session['telefono']
    else:
    # Si no está en la sesión, usamos el teléfono de la base de datos
        pedido.telefono = pedido.cliente.phone_number


    # Imprimir los datos que se están utilizando
    print("Dirección confirmada:", pedido.direccion)
    print("Teléfono confirmado:", pedido.telefono)

    # Guardar el pedido
    pedido.save()

    # Crear las líneas de pedido para cada producto en el carrito
    for linea_carrito in lineas:
        LineaPedido.objects.create(
            pedido=pedido,
            producto=linea_carrito.producto,
            cantidad=linea_carrito.cantidad,
            precio_unitario=linea_carrito.precio
        )

    # Vaciar el carrito de compras
    carrito.lineas.all().delete()

    messages.success(request, "Pedido confirmado exitosamente. ¡Gracias por tu compra!")

    # Redirigir al listado de pedidos del usuario actual
    return redirect('pedidos:listar_pedidos')
