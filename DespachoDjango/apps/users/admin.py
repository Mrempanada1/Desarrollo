from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, DueñoProfile, TrabajadorProfile, SupervisorProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'nombre', 'apellido', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'nombre', 'apellido')
    ordering = ('email',)

    # Definimos los fieldsets personalizados
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Campos básicos
        (_('Información Personal'), {'fields': (
            'nombre', 'apellido', 'telefono', 'direccion', 'avatar')}),  # Datos personales
        (_('Permisos'), {'fields': ('role', 'is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),  # Permisos y roles
        # Fechas importantes
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    # Campos para cuando se crea un usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nombre', 'apellido', 'role'),
        }),
    )

# Registro del perfil de Dueño


@admin.register(DueñoProfile)
class DueñoProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'nombre',
                    'apellido', 'telefono', 'direccion')
    search_fields = ('user__email', 'rut', 'nombre', 'apellido')

# Registro del perfil de Trabajador


@admin.register(TrabajadorProfile)
class TrabajadorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'nombre', 'apellido', 'email',
                    'direccion', 'disponibilidad', 'estado', 'asignacion')
    search_fields = ('user__email', 'rut', 'nombre', 'apellido')
    list_filter = ('estado', 'disponibilidad', 'asignacion')

# Registro del perfil de Supervisor


@admin.register(SupervisorProfile)
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'nombre', 'apellido', 'email',
                    'direccion', 'disponibilidad', 'estado', 'asignacion')
    search_fields = ('user__email', 'rut', 'nombre', 'apellido')
    list_filter = ('estado', 'disponibilidad', 'asignacion')
