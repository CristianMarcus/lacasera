from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen']

    def __init__(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance').id if kwargs.get('instance') else None
        super(ProductoForm, self).__init__(*args, **kwargs)

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        productos = Producto.objects.filter(nombre=nombre)
        if self.instance_id:
            productos = productos.exclude(id=self.instance_id)
        if productos.exists():
            raise forms.ValidationError('Ya existe un producto con ese nombre.')
        return nombre
