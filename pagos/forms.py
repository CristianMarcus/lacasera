# pagos/forms.py
from django import forms

class CheckoutForm(forms.Form):
    nombre = forms.CharField(max_length=100, label='Nombre')
    direccion = forms.CharField(widget=forms.Textarea, label='Dirección')
    ciudad = forms.CharField(max_length=100, label='Ciudad')
    telefono = forms.CharField(max_length=20, label='Teléfono')
