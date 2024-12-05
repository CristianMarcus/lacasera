# pedidos/urls.py

from django.urls import path
from pedidos.views import (
    realizar_pedido,
    listar_pedidos,
    detalle_pedido,
    confirmar_pago_efectivo,
    eliminar_pedido,
)


urlpatterns = [
    path('realizar/', realizar_pedido, name='realizar_pedido'),
    path('<int:pedido_id>/eliminar/', eliminar_pedido, name='eliminar_pedido'),
    path('', listar_pedidos, name='listar_pedidos'),
    path('<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
    path('confirmar-pago-efectivo/',confirmar_pago_efectivo, name='confirmar_pago_efectivo'),
]
