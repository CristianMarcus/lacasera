# productos/urls.py
from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('listar/', views.listar_productos, name='listar_productos'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:producto_id>/', views.eliminar_producto_admin, name='eliminar_producto_admin'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
]
