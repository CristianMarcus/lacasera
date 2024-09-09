from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pedidos_index'),  # Asegúrate de que la vista 'index' esté en 'views.py'
]
