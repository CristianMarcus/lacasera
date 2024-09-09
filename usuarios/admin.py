from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    model = Usuario
    # Aquí puedes personalizar la forma en que se muestran los campos en el admin
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('custom_field',)}),  # Agrega campos personalizados aquí
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('custom_field',)}),  # Agrega campos personalizados en el formulario de creación
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(Usuario, UsuarioAdmin)
