from django import forms
from .models import Carrito, LineaCarrito
from pedidos.models import Pedido


class CarritoForm(forms.ModelForm):
    class Meta:
        model = Carrito
        fields = ['usuario']

class LineaCarritoForm(forms.ModelForm):
    class Meta:
        model = LineaCarrito
        fields = ['carrito', 'producto', 'cantidad']



from django import forms
from pedidos.models import Pedido 

class PedidoContactoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion', 'telefono']  # Asegúrate de incluir los campos a actualizar
        labels = {
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

   

class AgregarCarritoForm(forms.Form):
    cantidad_total = forms.IntegerField(min_value=1, required=False, label='Cantidad Total')

    def __init__(self, *args, **kwargs):
        producto = kwargs.pop('producto', None)
        super().__init__(*args, **kwargs)

    
        






    

        
