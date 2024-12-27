from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Administración
    path('admin/', admin.site.urls),

    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),

    # Aplicaciones principales
    path('', include('core.urls')),  # Rutas de la app core
    path('usuarios/', include('usuarios.urls')),  # Rutas de la app usuarios
    path('productos/', include('productos.urls', namespace='productos')),  # Rutas de la app productos
    path('carritodecompras/', include('carritodecompras.urls', namespace='carritodecompras')),  # Carrito
    path('pagos/', include('pagos.urls')),  # Rutas de la app pagos
    path('pedidos/', include('pedidos.urls')),  # Rutas de la app pedidos
    path('promoOfertas/', include('promoOfertas.urls')),  # Rutas de la app promoOfertas
    path('historialcompras/', include('historialcompras.urls')),  # Historial de compras
]

# Archivos estáticos y de medios
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)