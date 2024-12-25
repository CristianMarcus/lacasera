from django import forms
from .models import Carrito, LineaCarrito
from productos.models import VariedadEmpanada


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
    def __init__(self, *args, **kwargs):
        producto = kwargs.pop('producto')
        super().__init__(*args, **kwargs)
        if producto.es_empanada:
            variedades = VariedadEmpanada.objects.filter(producto=producto)
            for variedad in variedades:
                self.fields[f'variedad_{variedad.id}'] = forms.IntegerField(
                    min_value=0, initial=0, label=f'{variedad.nombre_variedad}'
                )




    

        
