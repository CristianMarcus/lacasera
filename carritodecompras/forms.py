from django import forms
from .models import Carrito, LineaCarrito



class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ['usuario']

class LineaCarritoForm(forms.ModelForm):
    class Meta:
        model = LineaCarrito
        fields = ['carrito', 'producto', 'cantidad']

class PedidoContactoForm(forms.Form):
    direccion = forms.CharField(max_length=255, required=True, label="Dirección")
    telefono = forms.CharField(max_length=20, required=True, label="Teléfono")

class AgregarCarritoForm(forms.Form):
    cantidad_total = forms.IntegerField(min_value=1, required=False, label='Cantidad Total')

    def __init__(self, *args, **kwargs):
        producto = kwargs.pop('producto', None)
        super().__init__(*args, **kwargs)

    
        






    

        
