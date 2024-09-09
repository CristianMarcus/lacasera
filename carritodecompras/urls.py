from django.urls import path
from . import views

urlpatterns = [
    path('carritos/', views.CarritoListView.as_view(), name='carrito_list'),
    path('carritos/<int:pk>/', views.CarritoDetailView.as_view(), name='carrito_detail'),
    path('carritos/create/', views.CarritoCreateView.as_view(), name='carrito_create'),
    path('carritos/<int:pk>/update/', views.CarritoUpdateView.as_view(), name='carrito_update'),
    
    path('lineas-carrito/', views.LineaCarritoListView.as_view(), name='linea_carrito_list'),
    path('lineas-carrito/<int:pk>/', views.LineaCarritoDetailView.as_view(), name='linea_carrito_detail'),
    path('lineas-carrito/create/', views.LineaCarritoCreateView.as_view(), name='linea_carrito_create'),
    path('lineas-carrito/<int:pk>/update/', views.LineaCarritoUpdateView.as_view(), name='linea_carrito_update'),
]
