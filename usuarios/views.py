from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages  # Framework de mensajes
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UsuarioUpdateForm


class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  # El archivo HTML para el inicio de sesión
    authentication_form = CustomAuthenticationForm  # Formulario personalizado


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Usa el formulario personalizado
        if form.is_valid():
            user = form.save()  # Guarda el usuario en la base de datos
            user.is_staff = False  # Asegúrate de que no sea staff
            user.is_superuser = False  # Asegúrate de que no sea superusuario
            user.save()  # Guarda el usuario con los cambios de permisos
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Recupera la contraseña del formulario
            user = authenticate(username=username, password=password)  # Autentica al usuario
            if user is not None:
                login(request, user)  # Inicia sesión automáticamente
                messages.success(request, 'Registro exitoso. ¡Bienvenido!')
                return redirect('listar_productos')  # Redirige después de iniciar sesión
        else:
            messages.error(request, 'Hubo errores en el formulario. Por favor, corrígelos.')
    else:
        form = CustomUserCreationForm()  # Formulario vacío para GET
    return render(request, 'usuarios/registro.html', {'form': form})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UsuarioUpdateForm

@login_required
def actualizar_contacto(request):
    """
    Actualiza la información de contacto del usuario.
    Este método maneja tanto solicitudes normales como solicitudes AJAX.
    """
    user = request.user  # Usuario autenticado
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=user)  # Usa el formulario para actualizar
        if form.is_valid():
            form.save()  # Guarda los datos actualizados del usuario
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Si es una solicitud AJAX
                return JsonResponse({'success': True, 'message': "Información actualizada con éxito."})
            else:
                messages.success(request, "Información actualizada con éxito.")
                return redirect('carrito')  # Redirige al carrito u otra página
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Si es AJAX
                return JsonResponse({'success': False, 'errors': form.errors})
            messages.error(request, "Hubo un error al actualizar la información.")
    else:
        form = UsuarioUpdateForm(instance=user)  # Formulario prellenado con los datos del usuario actual

    return render(request, 'usuarios/actualizar_contacto.html', {'form': form})





