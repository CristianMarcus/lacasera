from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
# Create your views here.
from django.shortcuts import render

def login_view(request):
    # Lógica de la vista de inicio de sesión
    return render(request, 'usuarios/login.html')


def logout_view(request):
    """Cerrar sesión del usuario y redirigir a la página de inicio."""
    auth_logout(request)
    return redirect('home')  # Asegúrate de tener una ruta 'home' definida
