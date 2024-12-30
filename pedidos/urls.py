from django.urls import path
from .views import (
    realizar_pedido,
    listar_pedidos,
    detalle_pedido,
    confirmar_pago_efectivo,
    confirmar_pago,
    cambiar_estado_pedido,
    eliminar_pedido,
)

app_name = 'pedidos'

urlpatterns = [
    path('realizar/', realizar_pedido, name='realizar_pedido'),
    path('confirmar_pago/', confirmar_pago, name='confirmar_pago'),
    path('confirmar-pago-efectivo/', confirmar_pago_efectivo, name='confirmar_pago_efectivo'),
    path('<int:pedido_id>/eliminar/', eliminar_pedido, name='eliminar_pedido'),
    path('<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),  # Ruta correcta para el detalle del pedido
    path('', listar_pedidos, name='listar_pedidos'),
    path('<int:pedido_id>/cambiar_estado/<str:nuevo_estado>/', cambiar_estado_pedido, name='cambiar_estado_pedido'), # Ruta para cambiar el estado del pedido
]
