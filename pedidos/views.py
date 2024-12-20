from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from carritodecompras.models import Carrito # Modelos del carrito
from pedidos.models import Pedido, LineaPedido  # Modelos de pedidos
from productos.models import Producto  # Asegúrate de importar Producto


# Verificación de usuario administrador
def es_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(es_admin)  # Solo permitir a los administradores acceder a esta vista
def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = nuevo_estado
    pedido.save()
    messages.success(request, f'El estado del pedido {pedido_id} ha sido actualizado a {nuevo_estado}.')
    return redirect('listar_pedidos')

@login_required
def listar_pedidos(request):
    # Filtrar pedidos por el usuario actual 
    pedidos = Pedido.objects.filter(cliente=request.user)
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})

@login_required
def realizar_pedido(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)

    if not carrito.lineacarrito_set.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')
    
    # Crear el pedido
    pedido = Pedido.objects.create(usuario=request.user)
    for linea in carrito.lineacarrito_set.all():
        LineaPedido.objects.create(
            pedido=pedido,
            producto=linea.producto,
            cantidad=linea.cantidad
        )
    carrito.delete()  # Vaciar el carrito
    messages.success(request, "Pedido realizado con éxito.")
    return redirect('ver_carrito')

@login_required
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if es_admin(request.user) or pedido.usuario == request.user:
        pedido.delete()
        messages.success(request, "El pedido ha sido eliminado correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este pedido.")
    
    return redirect('listar_pedidos')

@login_required
def detalle_pedido(request, pedido_id):
    # Permitir acceso al administrador y al propietario del pedido
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if not request.user.is_superuser and pedido.cliente != request.user:
        return render(request, '403.html')  # Mostrar página 403 si el usuario no tiene permiso

    lineas = pedido.lineas.all()
    for linea in lineas:
        linea.subtotal = linea.precio_unitario * linea.cantidad
    total = sum(linea.subtotal for linea in lineas)  # Calcular el total del pedido

    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido, 'lineas': lineas, 'total': total})

@login_required
def confirmar_pago_efectivo(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)

    if not carrito.lineacarrito_set.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('carrito')

    # Crear el pedido
    pedido = Pedido.objects.create(usuario=request.user, estado="Pendiente")
    
    for linea in carrito.lineacarrito_set.all():
        # Verifica que cada línea tenga un producto asociado
        if linea.producto is not None:
            LineaPedido.objects.create(
                pedido=pedido,
                producto=linea.producto,
                cantidad=linea.cantidad
            )
        else:
            messages.error(request, "Algunas líneas en tu carrito no tienen un producto válido.")
            return redirect('carrito')

    # Vaciar el carrito
    carrito.delete()
    messages.success(request, "Pedido confirmado. Paga al recibir tu pedido.")
    return redirect('menu')

@login_required
def confirmar_pago(request):
    usuario = request.user
    carrito = Carrito.objects.get(usuario=usuario)
    if request.method == 'POST':
        total = carrito.get_total()  # Asegúrate de calcular el total correctamente

        # Crear el pedido
        pedido = Pedido.objects.create(
            cliente=usuario,
            estado="Pendiente",
            total=total
        )
        # Crear las líneas de pedido
        for linea in carrito.lineas.all():
            producto = get_object_or_404(Producto, nombre=linea.producto.nombre)
            LineaPedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=linea.cantidad,
                precio_unitario=linea.producto.precio
            )
        # Vaciar el carrito de compras
        carrito.lineas.all().delete()

        # Añadir mensaje de éxito
        messages.success(request, 'Pedido confirmado con éxito, ¡Gracias por tu compra!')

        # Redirigir a una página de confirmación o pedidos
        return redirect('listar_pedidos')  # O redirigir a una página de confirmación
    return render(request, 'pedidos/confirmar_pago.html', {'carrito': carrito})
