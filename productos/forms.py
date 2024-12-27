from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 
            'descripcion', 
            'precio_docena', 
            'precio_media_docena', 
            'precio_unidad', 
            'imagen', 
            'disponible', 
            'stock', 
            'categoria', 
            'es_empanada'
        ]

    def __init__(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance').id if kwargs.get('instance') else None
        super().__init__(*args, **kwargs)

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        productos = Producto.objects.filter(nombre=nombre)
        if self.instance_id:
            productos = productos.exclude(id=self.instance_id)
        if productos.exists():
            raise forms.ValidationError('Ya existe un producto con ese nombre.')
        return nombre

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('es_empanada'):
            if not all([cleaned_data.get('precio_docena'), cleaned_data.get('precio_media_docena'), cleaned_data.get('precio_unidad')]):
                raise forms.ValidationError('Debes proporcionar precios para docena, media docena y unidad si el producto es una empanada.')
        return cleaned_data
