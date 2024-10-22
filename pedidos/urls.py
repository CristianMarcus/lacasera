from django.urls import path
from .views import realizar_pedido, listar_pedidos, detalle_pedido

urlpatterns = [
    path('realizar/', realizar_pedido, name='realizar_pedido'),
    path('', listar_pedidos, name='listar_pedidos'),
    path('<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
]
