from django import forms
from .models import Vehiculo


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'año', 'color',
                  'patente', 'cliente']  # Campos del formulario
