from django import forms
from .models import Dueño, Vehiculo, Reparacion, Trabajador, Cita, Pago, Servicio, Proceso, Perfil
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Formulario para registrar la cuenta


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label='Confirmar contraseña')
    rol = forms.ChoiceField(choices=Perfil.ROLE_CHOICES, label='Rol')

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'rol']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        # Crea el perfil del usuario con el rol seleccionado
        perfil = Perfil(user=user, rol=self.cleaned_data['rol'])
        perfil.save()

        return user

# Formulario para el registro del dueño (cliente)


class DueñoForm(forms.ModelForm):
    class Meta:
        model = Dueño
        fields = ['rut', 'nombre', 'apellido',
                  'telefono', 'email', 'direccion']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Formulario para el registro de vehículos


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['patente', 'marca', 'modelo', 'año', 'color', 'kilometraje',
                  'tipo_combustible', 'fecha_ultima_revision', 'estado_vehiculo']
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'año': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_combustible': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ultima_revision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_vehiculo': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para el registro de reparaciones


class ReparacionForm(forms.ModelForm):
    class Meta:
        model = Reparacion
        fields = ['desc_problema', 'fecha_estimada_fin',
                  'estado_reparacion', 'costo_estimado']
        widgets = {
            'desc_problema': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_estimada_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_reparacion': forms.TextInput(attrs={'class': 'form-control'}),
            'costo_estimado': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Formulario para el registro de trabajadores


class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['rut', 'nombre', 'apellido', 'asignacion',
                  'telefono', 'email', 'direccion', 'disponibilidad', 'estado']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'asignacion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'disponibilidad': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario para la gestión de citas


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_y_hora', 'motivo',
                  'estado_cita', 'ubicacion', 'vehiculo']
        widgets = {
            'fecha_y_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control'}),
            'estado_cita': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
        }

        def clean_fecha_y_hora(self):
            fecha = self.cleaned_data.get('fecha_y_hora')
            if fecha < timezone.now():
                raise forms.ValidationError(
                    "La fecha de la cita no puede estar en el pasado.")
            return fecha


# Formulario para la gestion de servicios


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre_servicio', 'descripcion',
                  'costo', 'duracion_estimada', 'garantia']
        widgets = {
            'duracion_estimada': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario de pago


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto', 'metodo_pago', 'estado_pago', 'reparacion']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'estado_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'reparacion': forms.Select(attrs={'class': 'form-control'}),
        }


# Formulario para la gestion de procesos

class ProcesoForm(forms.ModelForm):
    class Meta:
        model = Proceso
        fields = ['fase_proceso', 'descripcion', 'fecha_inicio', 'fecha_fin',
                  'estado_proceso', 'prioridad', 'comentarios', 'trabajador']
        widgets = {
            'fase_proceso': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado_proceso': forms.TextInput(attrs={'class': 'form-control'}),
            'prioridad': forms.TextInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control'}),
            'trabajador': forms.Select(attrs={'class': 'form-control'}),
        }
