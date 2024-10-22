# carritodecompras/urls.py
from django.urls import path
from .views import (
    ver_carrito,
    agregar_al_carrito,
    eliminar_producto,
    ver_carrito_sesion,
    agregar_producto_sesion,
    eliminar_producto_sesion,
)

urlpatterns = [
    # Rutas para usuarios autenticados
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

    # Rutas para usuarios no autenticados
    path('carrito/sesion/', ver_carrito_sesion, name='ver_carrito_sesion'),
    path('carrito/sesion/agregar/<int:producto_id>/', agregar_producto_sesion, name='agregar_producto_sesion'),
    path('carrito/sesion/eliminar/<int:producto_id>/', eliminar_producto_sesion, name='eliminar_producto_sesion'),
]
