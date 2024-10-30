from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen']


    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if Producto.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError('Ya existe un producto con ese nombre.')
        return nombre