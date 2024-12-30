from django.urls import path
from .views import ver_historial

app_name = 'historialcompras'

urlpatterns = [
    
path('historial/', ver_historial, name='ver_historial'),

]



