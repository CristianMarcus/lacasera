from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import listar_productos, detalle_producto, crear_producto, editar_producto, eliminar_producto, menu
  # Import desde la app correcta

urlpatterns = [
    path('', menu, name='menu'),
    
    path('productos/', listar_productos, name='listar_productos'),
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('producto/nuevo/', crear_producto, name='crear_producto'),
    path('producto/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)