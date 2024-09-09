from django.contrib import admin
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # URL raíz dirigida a la aplicación `core`
    path('usuarios/', include('usuarios.urls')),
    path('productos/', include('productos.urls')),
    path('carritodecompras/', include('carritodecompras.urls')),
    path('pagos/', include('pagos.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('promoOfertas/', include('promoOfertas.urls')),
    path('historialcompras/', include('historialcompras.urls')),
]
