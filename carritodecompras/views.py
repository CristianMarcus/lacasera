from django.shortcuts import render, redirect, get_object_or_404
from .models import Carrito, LineaCarrito
from productos.models import Producto  # Asegúrate de que esto apunte correctamente a tus modelos
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Importa el decorador

@login_required  # Redirige a la página de inicio de sesión si el usuario no está autenticado
def carrito(request):
    # Lógica para mostrar el carrito de compras
    carrito = Carrito.objects.filter(usuario=request.user).first()  # Busca el carrito del usuario
    lineas_carrito = LineaCarrito.objects.filter(carrito=carrito) if carrito else []  # Evita errores si el carrito es None
    return render(request, 'carritodecompras/carrito.html', {'lineas_carrito': lineas_carrito})

@login_required  # Asegúrate de que solo los usuarios autenticados puedan agregar al carrito
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = Carrito.objects.filter(usuario=request.user).first()  # Busca el carrito del usuario
    if not carrito:
        carrito = Carrito(usuario=request.user)
        carrito.save()
    linea_carrito, created = LineaCarrito.objects.get_or_create(
        carrito=carrito, producto=producto,
        defaults={'cantidad': 1}
    )
    if not created:
        linea_carrito.cantidad += 1
        linea_carrito.save()
    messages.success(request, f'Producto {producto.nombre} agregado al carrito.')
    return redirect('carrito')

@login_required  # Asegúrate de que solo los usuarios autenticados puedan eliminar del carrito
def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = Carrito.objects.filter(usuario=request.user).first()  # Busca el carrito del usuario
    if carrito:
        try:
            linea_carrito = LineaCarrito.objects.get(carrito=carrito, producto=producto)
            linea_carrito.delete()
            messages.success(request, f'Producto {producto.nombre} eliminado del carrito.')
        except LineaCarrito.DoesNotExist:
            messages.error(request, 'El producto no está en el carrito.')
    else:
        messages.error(request, 'No tienes un carrito activo.')
    return redirect('carrito')
###Decorador login_required: He añadido el decorador @login_required a cada vista para asegurarnos de que solo los usuarios autenticados puedan acceder a estas funciones. Si un usuario no está autenticado, será redirigido a la página de inicio de sesión.

#Manejo de carrito vacío: En la vista carrito, se agregó una verificación para asegurar que lineas_carrito sea una lista vacía si carrito es None. Esto evita errores si el usuario no tiene un carrito creado.

#Manejo de errores en eliminar_del_carrito: Se añadió un mensaje de error si el usuario no tiene un carrito activo.