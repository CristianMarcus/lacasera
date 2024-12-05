from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from carritodecompras.models import Carrito, LineaCarrito  # Modelos del carrito
from pedidos.models import Pedido, LineaPedido  # Modelos de pedidos


# Verificación de usuario administrador
def es_admin(user):
    return user.is_superuser


@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.all()
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
    return redirect('listar_pedidos')

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
    pedido = get_object_or_404(Pedido, id=pedido_id)
    total = 0

    # Calculamos el total de los productos en el pedido
    for linea in pedido.lineas_pedido_pedidos.all():
        total += linea.producto.precio * linea.cantidad

    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido, 'total': total})

@login_required
def confirmar_pago_efectivo(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)

    if not carrito.lineacarrito_set.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')

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
            return redirect('ver_carrito')

    # Vaciar el carrito
    carrito.delete()
    messages.success(request, "Pedido confirmado. Paga al recibir tu pedido.")
    return redirect('menu')

