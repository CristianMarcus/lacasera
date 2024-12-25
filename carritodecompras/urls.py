from django.urls import path
from . import views

app_name = 'carritodecompras'

urlpatterns = [
    # Rutas principales del carrito
    path('', views.ver_carrito, name='ver_carrito'),  # Página principal del carrito
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar'),  # Agregar producto
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),  # Eliminar producto
    path('disminuir/<int:producto_id>/', views.disminuir_cantidad_producto, name='disminuir_cantidad_producto'),  # Disminuir cantidad
    path('incrementar/<int:producto_id>/', views.incrementar_cantidad_producto, name='incrementar_cantidad_producto'),  # Incrementar cantidad

    # Actualización de contacto
    path('actualizar_contacto_pedido/<int:pedido_id>/', views.actualizar_contacto_pedido, name='actualizar_contacto_pedido'),

    # Rutas para sesiones (usuarios no autenticados)
    path('sesion/', views.ver_carrito_sesion, name='ver_carrito_sesion'),
    path('sesion/agregar/<int:producto_id>/', views.agregar_producto_sesion, name='agregar_producto_sesion'),
    path('sesion/eliminar/<int:producto_id>/', views.eliminar_producto_sesion, name='eliminar_producto_sesion'),

    # Procesamiento de pagos
    path('procesar_pago_stripe/', views.procesar_pago_stripe, name='procesar_pago_stripe'),
    path('procesar_pago_mp/', views.procesar_pago_mp, name='procesar_pago_mp'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago'),

]
