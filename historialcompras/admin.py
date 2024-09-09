from django.contrib import admin
from .models import HistorialCompra

@admin.register(HistorialCompra)
class HistorialCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'pedido', 'fecha')
    list_filter = ('usuario', 'fecha')
    search_fields = ('usuario__username', 'pedido__id')
    ordering = ('-fecha',)
    readonly_fields = ('fecha',)
