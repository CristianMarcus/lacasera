from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Usuario





from django import forms
from django.contrib.auth.models import User

class UsuarioUpdateForm(forms.ModelForm):
    direccion = forms.CharField(max_length=255, required=True, label='Dirección')
    telefono = forms.CharField(max_length=15, required=True, label='Teléfono')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'direccion', 'telefono']




class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Usuario')  # Cambia 'username' a 'Usuario'
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)  # Cambia 'password' a 'Contraseña'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address')
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone_number': 'Número de teléfono',
            'address': 'Dirección',
        }
        help_texts = {
            'username': None,  # Elimina el texto de ayuda para el nombre de usuario
            'email': None,     # Elimina el texto de ayuda para el correo electrónico
            'password1': None, # Elimina el texto de ayuda para la contraseña
            'password2': None, # Elimina el texto de ayuda para la confirmación de contraseña
        }

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.is_staff = False  # Asegúrate de que no sea staff
        user.is_superuser = False  # Asegúrate de que no sea superusuario
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'address')
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone_number': 'Número de teléfono',
            'address': 'Dirección',
        }
        help_texts = {
            'username': None,
            'email': None,
        }
        

class contactForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['phone_number', 'address']
        
