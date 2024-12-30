from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from carritodecompras.models import Carrito  # Modelos del carrito
from pedidos.models import Pedido, LineaPedido  # Modelos de pedidos
from productos.models import Producto  # Asegúrate de importar Producto
from django.core.exceptions import PermissionDenied

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
    return redirect('pedidos:listar_pedidos')

@login_required
def listar_pedidos(request):
    if request.user.is_superuser:
        # Si el usuario es administrador, mostrar todos los pedidos
        pedidos = Pedido.objects.all()
    else:
        # Si el usuario no es administrador, filtrar pedidos por el usuario actual
        pedidos = Pedido.objects.filter(cliente=request.user)
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})

@login_required
def realizar_pedido(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)

    if not carrito.lineacarrito_set.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')
    
    # Crear el pedido
    pedido = Pedido.objects.create(cliente=request.user)
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

    if request.user.is_superuser or pedido.cliente == request.user:
        pedido.delete()
        messages.success(request, "El pedido ha sido eliminado correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este pedido.")
    
    return redirect('pedidos:listar_pedidos')

@login_required
def detalle_pedido(request, pedido_id):
    # Permitir acceso al administrador y al propietario del pedido
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if not request.user.is_superuser and pedido.cliente != request.user:
        raise PermissionDenied

    lineas = pedido.lineas.all()  # Obtiene todas las líneas del pedido
    total = sum(linea.get_subtotal() for linea in lineas)  # Usa el método del modelo para calcular subtotales

    return render(request, 'pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'lineas': lineas,
        'total': total
    })


@login_required
def confirmar_pago_efectivo(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)

    if not carrito.lineacarrito_set.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('carrito')

    # Crear el pedido
    pedido = Pedido.objects.create(cliente=request.user, estado="Pendiente")
    
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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pedido, LineaPedido
from carritodecompras.models import Carrito, LineaCarrito
from productos.models import Producto

@login_required
def confirmar_pago(request):
    usuario = request.user
    carrito = get_object_or_404(Carrito, usuario=usuario)
    if request.method == 'POST':
        total = sum(linea.get_subtotal() for linea in carrito.lineas.all())

        # Obtener el pedido pendiente existente
        pedido = Pedido.objects.filter(cliente=usuario, estado="Pendiente").first()

        if pedido is not None:
            # Actualizar el total del pedido existente
            pedido.total = total
            pedido.direccion = request.POST.get('direccion', usuario.address)
            pedido.telefono = request.POST.get('telefono', usuario.phone_number)
            pedido.save()
        else:
            # Crear un nuevo pedido si no existe ninguno pendiente
            pedido = Pedido.objects.create(
                cliente=usuario,
                estado="Pendiente",
                total=total,
                direccion=request.POST.get('direccion', usuario.address),
                telefono=request.POST.get('telefono', usuario.phone_number)
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
        return redirect('pedidos:listar_pedidos')

    return render(request, 'pedidos/confirmar_pago.html', {'carrito': carrito})
