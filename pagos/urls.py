from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='pagos_index'),  # Asegúrate de tener la vista 'index' en 'views.py'
]
