from django.shortcuts import render, get_object_or_404, redirect
from .models import Pedido, LineaPedido
from carritodecompras.models import Carrito, LineaCarrito

def realizar_pedido(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    pedido = Pedido.objects.create(usuario=request.user)
    for linea in carrito.lineacarro_set.all():
        LineaPedido.objects.create(pedido=pedido, producto=linea.producto, cantidad=linea.cantidad)
    carrito.delete()  # Elimina el carrito después de realizar el pedido
    return redirect('listar_pedidos')

def listar_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos': pedidos})

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})
