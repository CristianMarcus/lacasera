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
    cantidad_total = forms.IntegerField(min_value=1, required=False, label='Cantidad Total')

    def __init__(self, *args, **kwargs):
        producto = kwargs.pop('producto', None)
        super().__init__(*args, **kwargs)

        if producto and producto.es_empanada:
            variedades = VariedadEmpanada.objects.filter(producto=producto)
            for variedad in variedades:
                self.fields[f'variedad_{variedad.id}'] = forms.IntegerField(
                    min_value=0, required=False, label=variedad.nombre_variedad
                )
        






    

        
