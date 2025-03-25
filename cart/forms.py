from django import forms
from .models import Carrito

class PedidoForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=20)
    direccion = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Carrito
        fields = ['nombre', 'telefono', 'direccion']
