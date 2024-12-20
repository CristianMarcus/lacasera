from django.urls import path
from .views import ver_carrito, agregar_al_carrito, eliminar_producto, ver_carrito_sesion, agregar_producto_sesion, eliminar_producto_sesion, procesar_pago_stripe, procesar_pago_mp

urlpatterns = [
    path('', ver_carrito, name='carrito'),



   

    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('sesion/', ver_carrito_sesion, name='ver_carrito_sesion'),
    path('sesion/agregar/<int:producto_id>/', agregar_producto_sesion, name='agregar_producto_sesion'),
    path('sesion/eliminar/<int:producto_id>/', eliminar_producto_sesion, name='eliminar_producto_sesion'),
    path('procesar_pago_stripe/', procesar_pago_stripe, name='procesar_pago_stripe'),
    path('procesar_pago_mp/', procesar_pago_mp, name='procesar_pago_mp'),
]
