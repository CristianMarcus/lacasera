from django.contrib import admin
from .models import Producto, Categoria, VariedadEmpanada

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_docena', 'precio_media_docena', 'precio_unidad', 'stock', 'disponible')
    list_filter = ('disponible', 'categoria', 'es_empanada')
    list_editable = ('precio_docena', 'precio_media_docena', 'precio_unidad', 'stock', 'disponible')
    search_fields = ('nombre', 'categoria__nombre')
    prepopulated_fields = {'nombre': ('nombre',)}

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

class VariedadEmpanadaAdmin(admin.ModelAdmin):
    list_display = ('producto', 'nombre_variedad')
    search_fields = ('producto__nombre', 'nombre_variedad')

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(VariedadEmpanada, VariedadEmpanadaAdmin)
