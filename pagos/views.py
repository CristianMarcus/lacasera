from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from carritodecompras.models import Carrito, LineaCarrito
from pedidos.models import Pedido, LineaPedido
from django.conf import settings
import stripe
import mercadopago

# Configuración de claves
stripe.api_key = settings.STRIPE_SECRET_KEY
sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

@login_required
def checkout(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        return redirect('carrito')
    return render(request, 'pagos/checkout.html', {'carrito': carrito})

@login_required
def procesar_pago(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '')
        direccion = request.POST.get('direccion', '')
        ciudad = request.POST.get('ciudad', '')
        telefono = request.POST.get('telefono', '')
        metodo_pago = request.POST.get('metodo_pago', '')

        carrito = Carrito.objects.filter(usuario=request.user).first()
        if not carrito:
            return redirect('carrito')

        # Crear pedido
        pedido = Pedido.objects.create(
            usuario=request.user,
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            telefono=telefono,
            total=carrito.get_total(),
        )

        # Crear líneas de pedido
        lineas_carrito = LineaCarrito.objects.filter(carrito=carrito)
        for linea in lineas_carrito:
            LineaPedido.objects.create(
                pedido=pedido,
                producto=linea.producto.nombre,
                cantidad=linea.cantidad,
                precio_unitario=linea.producto.precio,
            )

        # Vaciar carrito después del pedido
        carrito.delete()

        # Redirigir a la vista de pago correspondiente
        if metodo_pago == 'tarjeta_credito' or metodo_pago == 'tarjeta_debito':
            return redirect('procesar_pago_stripe', pedido_id=pedido.id)
        elif metodo_pago == 'mercado_pago':
            return redirect('procesar_pago_mercadopago', pedido_id=pedido.id)

    return redirect('carrito')

@login_required
def procesar_pago_stripe(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=int(pedido.total * 100),  # Stripe usa céntimos
                currency='usd',
                description=f'Pago por Pedido {pedido.id}',
                source=token,
            )
            pedido.estado = 'Pagado'
            pedido.save()
            return redirect('pedido_exitoso', pedido_id=pedido.id)
        except stripe.error.CardError as e:
            return redirect('pago_fallido', pedido_id=pedido.id)
    return render(request, 'pagos/pago_stripe.html', {'pedido': pedido})

@login_required
def procesar_pago_mercadopago(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Crear preferencia de pago en MercadoPago
    preference_data = {
        "items": [
            {
                "title": f"Pedido {pedido.id}",
                "quantity": 1,
                "unit_price": float(pedido.total),
            }
        ],
        "payer": {
            "email": request.user.email
        },
        "back_urls": {
            "success": request.build_absolute_uri('pedido_exitoso'),
            "failure": request.build_absolute_uri('pago_fallido'),
            "pending": request.build_absolute_uri('pedido_pendiente')
        },
        "auto_return": "approved",
    }

    preference_response = sdk.preference().create(preference_data)
    response = preference_response.get("response", {})

    # Verificar si hay algún error en la respuesta de MercadoPago
    if 'id' not in response:
        error_message = response.get("message", "Error desconocido")
        return render(request, 'pagos/error.html', {
            'message': f'Error al crear la preferencia de pago en MercadoPago: {error_message}'
        })

    preference_id = response["id"]
    return render(request, 'pagos/pago_mercadopago.html', {
        'preference_id': preference_id,
        'MERCADOPAGO_PUBLIC_KEY': settings.MERCADOPAGO_PUBLIC_KEY,
    })

@login_required
def pedido_exitoso(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pagos/pedido_exitoso.html', {'pedido': pedido})

@login_required
def pago_fallido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pagos/pago_fallido.html', {'pedido': pedido})
