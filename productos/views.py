from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Asegúrate de importar Q
from .models import Producto
from .forms import ProductoForm
from carritodecompras.models import LineaCarrito

def menu(request):
    productos = Producto.objects.all()
    return render(request, 'productos/menu.html', {'productos': productos})

def listar_productos(request):
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')

    productos = Producto.objects.all().select_related('categoria')
    if query:
        productos = productos.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))
    if categoria_id:
        productos = productos.filter(categoria__id=categoria_id)

    return render(request, 'productos/listar_productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form})

@login_required
def eliminar_producto_admin(request, producto_id):
    # Obtener el producto a eliminar
    producto = get_object_or_404(Producto, pk=producto_id)
    
    # Eliminar el producto de la base de datos
    producto.delete()
    
    # Mostrar un mensaje de éxito
    messages.success(request, 'Producto eliminado exitosamente.')
    
    # Redirigir a la lista de productos
    return redirect('listar_productos')
