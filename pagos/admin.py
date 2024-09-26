# pagos/admin.py
from django.contrib import admin
from .models import MetodoPago, Transaccion, Pedido, LineaPedido

admin.site.register(MetodoPago)
admin.site.register(Transaccion)
admin.site.register(Pedido)
admin.site.register(LineaPedido)
