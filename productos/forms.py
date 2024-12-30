from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'disponible']

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        # Obtener la instancia del formulario
        instance_id = self.instance.id if self.instance else None

        # Verificar si ya existe un producto con el mismo nombre
        productos = Producto.objects.filter(nombre=nombre)
        if instance_id:
            productos = productos.exclude(id=instance_id)

        if productos.exists():
            raise forms.ValidationError('Ya existe un producto con ese nombre.')
        return nombre


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('es_empanada'):
            if not all([cleaned_data.get('precio_docena'), cleaned_data.get('precio_media_docena'), cleaned_data.get('precio_unidad')]):
                raise forms.ValidationError('Debes proporcionar precios para docena, media docena y unidad si el producto es una empanada.')
        return cleaned_data
