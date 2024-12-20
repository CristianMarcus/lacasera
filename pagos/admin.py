from django.contrib import admin
from .models import Pago  # Corrige las importaciones

class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'metodo_pago', 'estado', 'fecha_pago', 'monto']
    ordering = ['fecha_pago']
    readonly_fields = ['fecha_pago']
    list_filter = ['metodo_pago', 'estado']

admin.site.register(Pago, PagoAdmin)
