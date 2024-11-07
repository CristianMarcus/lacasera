# pagos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
    path('procesar_pago_stripe/<int:pedido_id>/', views.procesar_pago_stripe, name='procesar_pago_stripe'),
    path('procesar_pago_mercadopago/<int:pedido_id>/', views.procesar_pago_mercadopago, name='procesar_pago_mercadopago'),
    path('pedido_exitoso/<int:pedido_id>/', views.pedido_exitoso, name='pedido_exitoso'),
    path('pago_fallido/<int:pedido_id>/', views.pago_fallido, name='pago_fallido'),
]
