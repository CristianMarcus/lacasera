from django.contrib import admin
from .models import MetodoPago, Transaccion

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('id', 'pedido', 'metodo_pago', 'monto', 'fecha', 'completado')
    list_filter = ('metodo_pago', 'completado', 'fecha')
    search_fields = ('pedido__id', 'metodo_pago__nombre', 'monto')
    ordering = ('-fecha',)
    readonly_fields = ('fecha',)
