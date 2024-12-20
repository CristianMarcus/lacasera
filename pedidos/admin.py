from django.contrib import admin
from .models import Pedido, LineaPedido

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha_pedido', 'estado', 'total']
    ordering = ['fecha_pedido']
    search_fields = ['cliente__username']

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(LineaPedido)
