from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# urls.py
from django.conf import settings
from django.conf.urls.static import static







urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('', include('core.urls')),  # Enlaza con las URLs de la app core
    path('usuarios/', include('usuarios.urls')),
    path('productos/', include('productos.urls')),  # Enlaza con las URLs de la app productos
    path('carrito/', include('carritodecompras.urls')),  # Enlaza con las URLs de la app carrito
    path('pagos/', include('pagos.urls')),  # Enlaza con las URLs de la app pagos
    path('pedidos/', include('pedidos.urls')),  # Enlaza con las URLs de la app pedidos
    path('promoOfertas/', include('promoOfertas.urls')),  # Enlaza con las URLs de la app promoOfertas
    path('historialcompras/', include('historialcompras.urls')),  # Enlaza con las URLs de la app historialcompras
       
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
