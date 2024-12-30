from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import Producto
from .forms import ProductoForm
from carritodecompras.forms import AgregarCarritoForm
from carritodecompras.models import LineaCarrito, Carrito

# Verificar si el usuario es superusuario
def is_superuser(user):
    return user.is_superuser

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = AgregarCarritoForm(request.POST, producto=producto)
        if form.is_valid():
            # Obtén la cantidad total, predeterminada a 1 si no está definida
            cantidad_total = form.cleaned_data.get('cantidad_total', 1)

            if cantidad_total is None or cantidad_total <= 0:
                messages.error(request, "La cantidad debe ser mayor que cero.")
                return redirect('productos:detalle_producto', producto_id=producto.id)

            # Manejo de productos genéricos con un solo precio
            linea, created = LineaCarrito.objects.get_or_create(
                carrito=carrito, producto=producto,
                defaults={'cantidad': cantidad_total, 'precio_unidad': producto.precio}
            )
            if not created:
                linea.cantidad += cantidad_total
                linea.save()

            messages.success(request, f"{producto.nombre} ha sido agregado al carrito.")
            return redirect('carritodecompras:ver_carrito')

    form = AgregarCarritoForm(producto=producto)
    return render(request, 'productos/detalle_producto.html', {'producto': producto, 'form': form})



def menu(request):
    productos = Producto.objects.all()
    return render(request, 'productos/menu.html', {'productos': productos})




@user_passes_test(is_superuser, login_url='productos:menu')
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
    form = AgregarCarritoForm(producto=producto)

    return render(request, 'productos/detalle_producto.html', {'producto': producto, 'form': form})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado exitosamente.')
            return redirect('productos:listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            producto_existente = Producto.objects.filter(nombre=nombre).exclude(id=producto_id).first()
            if producto_existente:
                messages.error(request, "Ya existe un producto con este nombre. Usa un nombre diferente.")
            else:
                form.save()
                messages.success(request, "Producto actualizado con éxito.")
                return redirect('productos:listar_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

@login_required
def eliminar_producto_admin(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado exitosamente.')
    return redirect('productos:listar_productos')
