from django.contrib import admin
from .models import Promocion

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descuento', 'fecha_inicio', 'fecha_fin')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('nombre',)
    filter_horizontal = ('productos',)  # Para manejar la relación Many-to-Many en el admin

