from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    # Otras URLs específicas de la app productos
]
