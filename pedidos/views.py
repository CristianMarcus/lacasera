from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from carritodecompras.models import Carrito, LineaCarrito
from pedidos.models import Pedido, LineaPedido
from productos.models import Producto
from django.core.exceptions import PermissionDenied

# Verificación de usuario administrador
def es_admin(user):
    """
    Comprueba si el usuario es administrador.
    """
    return user.is_superuser

@login_required
@user_passes_test(es_admin)
def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    """
    Cambia el estado de un pedido (solo para administradores).
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = nuevo_estado
    pedido.save()
    messages.success(request, f'El estado del pedido {pedido_id} ha sido actualizado a {nuevo_estado}.')
    return redirect('pedidos:listar_pedidos')

@login_required
def listar_pedidos(request):
    # Obtener los pedidos del usuario actual
    pedidos = Pedido.objects.filter(cliente=request.user)

    # Verificar si hay datos en la sesión para dirección y teléfono
    for pedido in pedidos:
        if 'direccion' in request.session and 'telefono' in request.session:
            # Actualizar la dirección y el teléfono del pedido con los datos de la sesión
            pedido.direccion = request.session['direccion']
            pedido.telefono = request.session['telefono']
        else:
            # Si no están en la sesión, usamos los datos de la base de datos
            pedido.direccion = pedido.cliente.address
            pedido.telefono = pedido.cliente.phone_number

    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})


@login_required
def realizar_pedido(request):
    """
    Convierte el contenido del carrito en un pedido y crea las líneas asociadas.
    """
    carrito = get_object_or_404(Carrito, usuario=request.user)

    # Validar si el carrito tiene productos
    if not carrito.lineacarrito_set.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('carritodecompras:ver_carrito')

    # Crear el pedido
    pedido = Pedido.objects.create(cliente=request.user, estado="Pendiente")

    # Asociar las líneas del carrito al pedido
    for linea_carrito in carrito.lineacarrito_set.all():
        LineaPedido.objects.create(
            pedido=pedido,
            producto=linea_carrito.producto,
            cantidad=linea_carrito.cantidad,
            precio_unitario=linea_carrito.producto.precio
        )
        print(f"Línea creada: Producto {linea_carrito.producto.nombre}, Cantidad {linea_carrito.cantidad}")
        lineas = pedido.lineas.all()
        print(f"Pedido {pedido.id} tiene {lineas.count()} líneas asociadas.")


    # Calcular el total del pedido
    pedido.calcular_total()

    # Vaciar el carrito
    carrito.lineacarrito_set.all().delete()

    messages.success(request, "Pedido realizado con éxito.")
    return redirect('pedidos:listar_pedidos')





@login_required
def eliminar_pedido(request, pedido_id):
    """
    Elimina un pedido si el usuario tiene permiso.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.user.is_superuser or pedido.cliente == request.user:
        pedido.delete()
        messages.success(request, "El pedido ha sido eliminado correctamente.")
    else:
        messages.error(request, "No tienes permiso para eliminar este pedido.")

    return redirect('pedidos:listar_pedidos')

from django.http import JsonResponse

@login_required
def detalle_pedido(request, pedido_id):
    """
    Muestra el detalle de un pedido específico.
    """
    # Obtener el pedido solicitado
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Verificar permisos para acceder al pedido
    if not request.user.is_superuser and pedido.cliente != request.user:
        raise PermissionDenied("No tienes permiso para ver este pedido.")

    # Obtener las líneas asociadas al pedido
    lineas = pedido.lineas.all()

    # Validar si hay líneas asociadas
    if not lineas.exists():
        messages.warning(request, "Este pedido no tiene líneas asociadas.")

    # Calcular el total del pedido usando las líneas
    total = sum(linea.get_subtotal() for linea in lineas)

    # Serializar las líneas en una lista de diccionarios para depuración o consumo adicional
    lineas_serializadas = [
        {
            "producto": linea.producto.nombre,
            "cantidad": linea.cantidad,
            "precio_unitario": float(linea.precio_unitario),
            "subtotal": float(linea.get_subtotal())
        }
        for linea in lineas
    ]

    # Agregar validación adicional: Mostrar mensaje si no hay líneas
    if not lineas_serializadas:
        messages.error(request, "No hay productos en este pedido. Verifica su creación o contenido.")

    # Renderizar la plantilla con el contexto adecuado
    return render(request, 'pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'lineas': lineas,
        'total': total,
        'lineas_serializadas': lineas_serializadas
    })


@login_required
def confirmar_pago(request):
    usuario = request.user
    carrito = get_object_or_404(Carrito, usuario=usuario)
    if request.method == 'POST':
        total = sum(linea.get_subtotal() for linea in carrito.lineas.all())

        # Obtener el pedido pendiente existente o crear uno nuevo
        pedido, created = Pedido.objects.get_or_create(
            cliente=usuario,
            estado="Pendiente",
            defaults={
                'total': total,
                'direccion': request.POST.get('direccion', usuario.address),
                'telefono': request.POST.get('telefono', usuario.phone_number),
            }
        )

        if not created:
            # Si el pedido ya existía, actualiza los datos con los del formulario
            pedido.total = total
            pedido.direccion = request.POST.get('direccion', usuario.address)
            pedido.telefono = request.POST.get('telefono', usuario.phone_number)
            pedido.save()

        # Crear las líneas de pedido
        for linea in carrito.lineas.all():
            LineaPedido.objects.create(
                pedido=pedido,
                producto=linea.producto,
                cantidad=linea.cantidad,
                precio_unitario=linea.precio
            )

        # Vaciar el carrito
        carrito.lineas.all().delete()

        messages.success(request, "Pedido confirmado con éxito.")
        return redirect('pedidos:listar_pedidos')

    return render(request, 'pedidos/confirmar_pago.html', {'carrito': carrito})


