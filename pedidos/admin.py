from django.contrib import admin
from .models import Pedido, LineaPedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'estado')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('usuario__username', 'estado')
    ordering = ('-fecha_pedido',)
    readonly_fields = ('fecha_pedido',)

@admin.register(LineaPedido)
class LineaPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad')
    list_filter = ('pedido', 'producto')
    search_fields = ('pedido__id', 'producto__nombre')
    ordering = ('pedido',)

