from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages  # Importa el framework de mensajes  # Importa el modelo Pedido
from pedidos.models import Pedido  # Importa correctamente desde la app pedidos

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  # El archivo HTML que contiene el formulario de inicio de sesión
    authentication_form = CustomAuthenticationForm  # Usa el formulario personalizado

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Usa el formulario personalizado
        if form.is_valid():
            user = form.save()  # Guarda el usuario en la base de datos
            user.is_staff = False  # Asegúrate de que no sea staff
            user.is_superuser = False  # Asegúrate de que no sea superusuario
            user.save()  # Guarda el usuario con los cambios de permisos
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # Asegúrate de que este campo esté en tu formulario
            user = authenticate(username=username, password=password)  # Autentica al usuario
            if user is not None:
                login(request, user)  # Inicia sesión automáticamente al usuario
                messages.success(request, 'Registro exitoso. ¡Bienvenido!')
                return redirect('listar_productos')  # Redirige después de iniciar sesión
        else:
            messages.error(request, 'Hubo errores en el formulario. Por favor, corrígelos.')
    else:
        form = CustomUserCreationForm()  # Usa el formulario personalizado
    return render(request, 'usuarios/registro.html', {'form': form})  # Renderiza la plantilla de registro


from django.contrib.auth.decorators import login_required
from .forms import UsuarioUpdateForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UsuarioUpdateForm
from django.contrib import messages

@login_required
def actualizar_contacto(request):
    user = request.user
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Actualizar los pedidos pendientes con los nuevos datos
            Pedido.objects.filter(cliente=user, estado="Pendiente").update(
                direccion=user.address,
                telefono=user.phone_number
            )
            messages.success(request, "Información actualizada con éxito.")
            return redirect('carritodecompras:ver_carrito')
        else:
            messages.error(request, "Hubo un error al actualizar la información.")
    else:
        form = UsuarioUpdateForm(instance=user)

    return render(request, 'usuarios/actualizar_contacto.html', {'form': form})







