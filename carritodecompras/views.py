from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from productos.models import Producto
from .models import LineaCarrito, Carrito
from .utils import obtener_carrito_usuario, actualizar_sesion_carrito
from django.contrib.messages import get_messages


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Carrito
from pedidos.models import Pedido
from .forms import PedidoContactoForm

@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    lineas = carrito.lineas.all()
    total_items = sum(linea.cantidad for linea in lineas)
    total_precio = sum(linea.get_subtotal() for linea in lineas)

    # Obtener el pedido en estado "Pendiente" o crear uno nuevo si no existe
    pedido = Pedido.objects.filter(cliente=request.user, estado="Pendiente").first()
    if not pedido:
        pedido = Pedido.objects.create(cliente=request.user, estado="Pendiente", total=total_precio)
    else:
        # Asegúrate de actualizar el total del pedido
        pedido.total = total_precio
        pedido.save()

    # Usar los datos del usuario si los campos del pedido están vacíos
    direccion = pedido.direccion or request.user.address
    telefono = pedido.telefono or request.user.phone_number

    form = PedidoContactoForm(initial={
        'direccion': direccion,
        'telefono': telefono,
    })

    return render(request, 'ver_carrito.html', {
        'carrito': carrito,
        'lineas': lineas,
        'total_items': total_items,
        'total_precio': total_precio,
        'form': form,
        'pedido': pedido
    })





@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    cantidad = int(request.POST.get('cantidad', 1))

    linea, created = LineaCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    if created:
        linea.cantidad = cantidad
    else:
        linea.cantidad += cantidad

    linea.save()
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


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PedidoContactoForm
from pedidos.models import Pedido

@login_required
def actualizar_contacto_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        form = PedidoContactoForm(request.POST)
        if form.is_valid():
            print(f"Datos antes de actualizar: Dirección: {pedido.direccion}, Teléfono: {pedido.telefono}")
            pedido.direccion = form.cleaned_data['direccion']
            pedido.telefono = form.cleaned_data['telefono']
            pedido.save()
            print(f"Datos después de actualizar: Dirección: {pedido.direccion}, Teléfono: {pedido.telefono}")
            return JsonResponse({'success': True})
        else:
            print(f"Errores del formulario: {form.errors}")
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PedidoContactoForm(initial={
            'direccion': pedido.direccion,
            'telefono': pedido.telefono,
        })
    
    return render(request, 'carritodecompras/actualizar_contacto_pedido.html', {'form': form, 'pedido': pedido})
