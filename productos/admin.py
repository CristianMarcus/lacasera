from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria', 'disponible', 'stock')
    list_filter = ('disponible', 'categoria')
    search_fields = ('nombre',)
    list_editable = ('precio', 'disponible', 'stock')  # Para permitir la edición directa en la lista
