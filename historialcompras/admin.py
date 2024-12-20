from django.contrib import admin
from .models import HistorialCompra

class HistorialCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'pedido', 'fecha']
    ordering = ['fecha']
    readonly_fields = ['fecha']
    list_filter = ['usuario', 'fecha']

admin.site.register(HistorialCompra, HistorialCompraAdmin)
