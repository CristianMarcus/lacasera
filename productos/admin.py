from django.contrib import admin
from .models import Producto, Categoria

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'precio', 'descripcion', 'disponible', 'stock', 'categoria')  # Ajusta los campos a los existentes
    list_filter = ('disponible', 'categoria')  # Elimina 'es_empanada'
    list_editable = ('precio', 'stock', 'disponible')  # Ajusta los campos editables a los que existen
    search_fields = ('nombre', 'descripcion')

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
