# pagos/admin.py

from django.contrib import admin
from .models import Pedido, LineaPedido

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'estado', 'total')
    list_filter = ('estado', 'fecha_pedido')
    readonly_fields = ('fecha_pedido',)
    ordering = ('fecha_pedido',)

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(LineaPedido)
