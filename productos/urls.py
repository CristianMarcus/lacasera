from django.urls import path
from .views import menu, listar_productos, detalle_producto, crear_producto, editar_producto, eliminar_producto_admin

urlpatterns = [
    path('', menu, name='menu'),
    path('productos/', listar_productos, name='listar_productos'),
    path('productos/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('productos/nuevo/', crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto_admin, name='eliminar_producto_admin'),
]
