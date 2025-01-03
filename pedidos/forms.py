from django import forms
from pedidos.models import Pedido

class PedidoContactoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion', 'telefono']
        labels = {
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configura campos vacíos por defecto
        self.fields['direccion'].initial = ''
        self.fields['telefono'].initial = ''
