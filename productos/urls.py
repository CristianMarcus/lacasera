from django.urls import path
from . import views

urlpatterns = [
    # Aquí puedes definir las rutas específicas para la aplicación productos
    path('', views.index, name='productos_index'),  # Ejemplo de ruta
]
