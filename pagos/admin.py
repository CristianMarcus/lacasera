# pagos/admin.py
from django.contrib import admin
from pedidos.models import Pedido  # Importar el modelo Pedido
from pedidos.admin import PedidoAdmin  # Importar la clase PedidoAdmin si la tienes personalizada

# Registrar el modelo Pedido con la clase de administración personalizada

