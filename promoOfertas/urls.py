from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='promociones_index'),  # Asegúrate de que la vista 'index' esté definida en 'views.py'
]
