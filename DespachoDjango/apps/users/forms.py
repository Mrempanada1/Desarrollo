from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User, DueñoProfile, TrabajadorProfile, SupervisorProfile

# Formulario para registrar un nuevo Dueño


class DueñoForm(UserCreationForm):
    rut = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    telefono = forms.CharField(max_length=20)
    direccion = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido',
                  'telefono', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'dueño'
        if commit:
            user.save()
            DueñoProfile.objects.create(
                user=user,
                rut=self.cleaned_data['rut'],
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                telefono=self.cleaned_data['telefono'],
                direccion=self.cleaned_data['direccion'],
            )
        return user

# Formulario para registrar un nuevo Trabajador


class TrabajadorForm(UserCreationForm):
    rut = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    email = forms.EmailField()
    direccion = forms.CharField(max_length=255)
    disponibilidad = forms.CharField(max_length=255)
    estado = forms.CharField(max_length=50)
    asignacion = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido',
                  'telefono', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'trabajador'
        if commit:
            user.save()
            TrabajadorProfile.objects.create(
                user=user,
                rut=self.cleaned_data['rut'],
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                email=self.cleaned_data['email'],
                direccion=self.cleaned_data['direccion'],
                disponibilidad=self.cleaned_data['disponibilidad'],
                estado=self.cleaned_data['estado'],
                asignacion=self.cleaned_data['asignacion'],
            )
        return user

# Formulario para registrar un nuevo Supervisor


class SupervisorForm(UserCreationForm):
    rut = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    email = forms.EmailField()
    direccion = forms.CharField(max_length=255)
    disponibilidad = forms.CharField(max_length=255)
    estado = forms.CharField(max_length=50)
    asignacion = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido',
                  'telefono', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'supervisor'
        if commit:
            user.save()
            SupervisorProfile.objects.create(
                user=user,
                rut=self.cleaned_data['rut'],
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                email=self.cleaned_data['email'],
                direccion=self.cleaned_data['direccion'],
                disponibilidad=self.cleaned_data['disponibilidad'],
                estado=self.cleaned_data['estado'],
                asignacion=self.cleaned_data['asignacion'],
            )
        return user

# Formulario para actualizar la información de un Dueño


class DueñoUpdateForm(ModelForm):
    rut = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    telefono = forms.CharField(max_length=20)
    direccion = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'dueño_profile'):
            profile = self.instance.dueño_profile
            self.fields['rut'].initial = profile.rut
            self.fields['nombre'].initial = profile.nombre
            self.fields['apellido'].initial = profile.apellido
            self.fields['telefono'].initial = profile.telefono
            self.fields['direccion'].initial = profile.direccion

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = self.instance.dueño_profile
            profile.rut = self.cleaned_data['rut']
            profile.nombre = self.cleaned_data['nombre']
            profile.apellido = self.cleaned_data['apellido']
            profile.telefono = self.cleaned_data['telefono']
            profile.direccion = self.cleaned_data['direccion']
            profile.save()
        return user

# Formulario para actualizar la información de un Trabajador


class TrabajadorUpdateForm(ModelForm):
    rut = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    email = forms.EmailField()
    direccion = forms.CharField(max_length=255)
    disponibilidad = forms.CharField(max_length=255)
    estado = forms.CharField(max_length=50)
    asignacion = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'trabajador_profile'):
            profile = self.instance.trabajador_profile
            self.fields['rut'].initial = profile.rut
            self.fields['nombre'].initial = profile.nombre
            self.fields['apellido'].initial = profile.apellido
            self.fields['email'].initial = profile.email
            self.fields['direccion'].initial = profile.direccion
            self.fields['disponibilidad'].initial = profile.disponibilidad
            self.fields['estado'].initial = profile.estado
            self.fields['asignacion'].initial = profile.asignacion

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = self.instance.trabajador_profile
            profile.rut = self.cleaned_data['rut']
            profile.nombre = self.cleaned_data['nombre']
            profile.apellido = self.cleaned_data['apellido']
            profile.email = self.cleaned_data['email']
            profile.direccion = self.cleaned_data['direccion']
            profile.disponibilidad = self.cleaned_data['disponibilidad']
            profile.estado = self.cleaned_data['estado']
            profile.asignacion = self.cleaned_data['asignacion']
            profile.save()
        return user

# Formulario para actualizar la información de un Supervisor


class SupervisorUpdateForm(ModelForm):
    rut = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=255)
    apellido = forms.CharField(max_length=255)
    email = forms.EmailField()
    direccion = forms.CharField(max_length=255)
    disponibilidad = forms.CharField(max_length=255)
    estado = forms.CharField(max_length=50)
    asignacion = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'telefono')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'supervisor_profile'):
            profile = self.instance.supervisor_profile
            self.fields['rut'].initial = profile.rut
            self.fields['nombre'].initial = profile.nombre
            self.fields['apellido'].initial = profile.apellido
            self.fields['email'].initial = profile.email
            self.fields['direccion'].initial = profile.direccion
            self.fields['disponibilidad'].initial = profile.disponibilidad
            self.fields['estado'].initial = profile.estado
            self.fields['asignacion'].initial = profile.asignacion

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = self.instance.supervisor_profile
            profile.rut = self.cleaned_data['rut']
            profile.nombre = self.cleaned_data['nombre']
            profile.apellido = self.cleaned_data['apellido']
            profile.email = self.cleaned_data['email']
            profile.direccion = self.cleaned_data['direccion']
            profile.disponibilidad = self.cleaned_data['disponibilidad']
            profile.estado = self.cleaned_data['estado']
            profile.asignacion = self.cleaned_data['asignacion']
            profile.save()
        return user
