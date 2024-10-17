from django import forms
from .models import Dueño, Vehiculo, Trabajador, Cita, Pago, Servicio, Proceso, Perfil, Cotizacion, DetalleCotizacion, Notificacion
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# Get the custom user model
User = get_user_model()

# Formulario para el registro del trabajador por parte de un administrador


class AdminTrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['rut', 'nombre', 'apellido', 'asignacion',
                  'telefono', 'email', 'direccion', 'disponibilidad', 'estado', 'rol']
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
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Asegúrate de que solo los administradores puedan elegir el rol
        if not self.request.user.is_superuser:
            self.fields['rol'].disabled = True

# Formulario para registrar la cuenta


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label='Confirmar contraseña')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
                  'password', 'password_confirm']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está en uso.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8 or not any(char.isdigit() for char in password):
            raise forms.ValidationError(
                "La contraseña debe tener al menos 8 caracteres y al menos un número.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            perfil = Perfil(user=user, rol='Cliente')  # Rol predeterminado
            perfil.save()

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

# Formulario para el registro de trabajadores


class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['rut', 'nombre', 'apellido', 'telefono', 'email',
                  'direccion', 'disponibilidad', 'estado', 'perfil', 'rol']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'disponibilidad': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'perfil': forms.Select(attrs={'class': 'form-control'}),
            'rol': forms.TextInput(attrs={'class': 'form-control'}),
        }
    

# Formulario para el registro de vehículos


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['patente', 'marca', 'modelo', 'año', 'color',
                  'kilometraje', 'tipo_combustible', 'fecha_ultima_revision', 'estado_vehiculo']
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'año': forms.NumberInput(attrs={'class': 'form-control', 'min': '1886'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_combustible': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ultima_revision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_vehiculo': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Formulario para la gestión de citas


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha_y_hora', 'motivo',
                  'estado_cita', 'ubicacion', 'vehiculo']
        widgets = {
            'fecha_y_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'estado_cita': forms.Select(attrs={'class': 'form-control'}),
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
            'nombre_servicio': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracion_estimada': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'garantia': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Formulario de pago


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['monto', 'metodo_pago', 'estado_pago', 'proceso']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'fecha_pago': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_pago': forms.Select(attrs={'class': 'form-control'}),
            'proceso': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario para la gestion de procesos


class ProcesoForm(forms.ModelForm):
    class Meta:
        model = Proceso
        fields = ['fase_proceso', 'descripcion', 'fecha_inicio', 'fecha_fin',
                  'estado_proceso', 'prioridad', 'comentarios', 'notificaciones', 'trabajador']
        widgets = {
            'fase_proceso': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_proceso': forms.TextInput(attrs={'class': 'form-control'}),
            'prioridad': forms.TextInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'notificaciones': forms.Select(attrs={'class': 'form-control'}),
            'trabajador': forms.Select(attrs={'class': 'form-control'}),
        }


# Formulario de notificaciones


class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        # Asegúrate de que los campos coincidan con los del modelo
        fields = ['mensaje', 'estado', 'proceso']
        widgets = {
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'proceso': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario de cotizacion


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['descripcion', 'monto_total', 'estado', 'vehiculo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
        }

# Formulario de detalle de cotización


class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = ['cotizacion', 'servicio']
        widgets = {
            'cotizacion': forms.Select(attrs={'class': 'form-control'}),
            'servicio': forms.Select(attrs={'class': 'form-control'}),
        }
