from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import authenticate, login
from .models import Dueño, Vehiculo, Reparacion, Trabajador, Cita, Pago, Servicio, Proceso, Perfil
from .forms import DueñoForm, VehiculoForm, ReparacionForm, TrabajadorForm, CitaForm, ServicioForm, PagoForm, ProcesoForm, UserRegistrationForm
from openpyxl import Workbook
import pandas as pd

# Perfiles


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    instance.perfil.save()

# Verifica si el usuario es administrador

def es_admin(user):
    return user.is_staff or user.groups.filter(name='Administradores').exists()

# Vista de inicio


def inicio(request):
    return render(request, 'inicio.html')

# Vista del login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Mensaje de éxito
            messages.success(request, f"Bienvenido {user.username}!")
            # Redirigir a la página de inicio o cualquier otra página
            return redirect('inicio')
        else:
            # Mensaje de error
            messages.error(
                request, 'Nombre de usuario o contraseña incorrectos')
            # Redirigir de nuevo al formulario de login
            return redirect('login')
    return render(request, 'login.html')


# Mi cuenta

@login_required
def mi_cuenta(request):
    # Verificar si el usuario es un dueño
    if not (hasattr(request.user, 'dueño') or hasattr(request.user, 'trabajador') or hasattr(request.user, 'administrador')):
        return HttpResponseForbidden('No tienes permiso para ver esta página.')

    dueño = request.user.dueño
    vehiculos = dueño.vehiculo_set.all()
    reparaciones = Reparacion.objects.filter(vehiculo__dueño=dueño)
    pagos = Pago.objects.filter(reparacion__vehiculo__dueño=dueño)

    return render(request, 'dueños/mi_cuenta.html', {
        'dueño': dueño,
        'vehiculos': vehiculos,
        'reparaciones': reparaciones,
        'pagos': pagos
    })

# Usuario


def registrar_usuario(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Crear el usuario
            user = User.objects.create_user(username=username, password=password)
            
            # Mensaje de alerta
            messages.success(request, 'Usuario registrado con éxito. Ahora puedes registrar un dueño.')

            # Autenticar y loguear al usuario automaticamente
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Aqui se asegura que el usuario creado se loguee automáticamente.

            # Redirigir a la pagina de login
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'registrar_usuario.html', {'form': form})

# Gestión de Clientes


@login_required
def lista_dueños(request):
    dueños = Dueño.objects.all()
    return render(request, 'dueños/lista_dueños.html', {'dueños': dueños})


@login_required
def registrar_dueño(request):
    if request.method == 'POST':
        form = DueñoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dueño registrado correctamente.')
            return redirect('lista_dueños')
        else:
            messages.error(
                request, 'Por favor corrige los errores en el formulario.')
    else:
        form = DueñoForm()

    return render(request, 'dueños/registrar_dueño.html', {'form': form})


@login_required
def editar_dueño(request, pk):
    dueño = get_object_or_404(Dueño, pk=pk)
    if request.method == 'POST':
        form = DueñoForm(request.POST, instance=dueño)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dueño actualizado correctamente.')
            return redirect('lista_dueños')
    else:
        form = DueñoForm(instance=dueño)
    return render(request, 'dueños/editar_dueño.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def eliminar_dueño(request, dueño_id):
    dueño = get_object_or_404(Dueño, id=dueño_id)
    dueño.delete()
    messages.success(request, 'Dueño eliminado correctamente.')
    return redirect(reverse('lista_dueños'))

# Gestión de Vehículos


@login_required
def lista_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculos/lista_vehiculos.html', {'vehiculos': vehiculos})


@login_required
def registrar_vehiculo(request):
    # Verificar si el usuario tiene un perfil de dueño
    if not hasattr(request.user, 'dueño'):
        return HttpResponseForbidden('No tienes permiso para registrar un vehículo.')

    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.dueño = request.user.dueño  # Asignar el dueño que ha iniciado sesión
            vehiculo.save()
            messages.success(request, 'Vehículo registrado correctamente.')
            return redirect('lista_vehiculos')
    else:
        form = VehiculoForm()

    return render(request, 'vehiculos/registrar_vehiculo.html', {'form': form})


@login_required
def editar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado correctamente.')
            return redirect('lista_vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiculos/editar_vehiculo.html', {'form': form})



# Gestión de Reparaciones


@login_required
def lista_reparaciones(request):
    reparaciones = Reparacion.objects.all()
    return render(request, 'reparaciones/lista_reparaciones.html', {'reparaciones': reparaciones})


@login_required
@user_passes_test(es_admin)
def registrar_reparacion(request):
    if request.method == 'POST':
        form = ReparacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reparación registrada correctamente.')
            return redirect('lista_reparaciones')
    else:
        form = ReparacionForm()
    return render(request, 'reparaciones/registrar_reparacion.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def editar_reparacion(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    if request.method == 'POST':
        form = ReparacionForm(request.POST, instance=reparacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reparación actualizada correctamente.')
            return redirect('lista_reparaciones')
    else:
        form = ReparacionForm(instance=reparacion)
    return render(request, 'reparaciones/editar_reparacion.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def eliminar_reparacion(request, pk):
    reparacion = get_object_or_404(Reparacion, pk=pk)
    reparacion.delete()
    messages.success(request, 'Reparación eliminada correctamente.')
    return redirect('lista_reparaciones')

# Gestión de Citas


@login_required
def lista_citas(request):
    citas = Cita.objects.all()
    return render(request, 'citas/lista_citas.html', {'citas': citas})


@login_required
def registrar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita registrada correctamente.')
            return redirect('lista_citas')
    else:
        form = CitaForm()
    return render(request, 'citas/registrar_cita.html', {'form': form})


@login_required
def editar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada correctamente.')
            return redirect('lista_citas')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'citas/editar_cita.html', {'form': form})


@login_required
def eliminar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    cita.delete()
    messages.success(request, 'Cita eliminada correctamente.')
    return redirect('lista_citas')

# Gestión de Pagos


@login_required
def lista_pagos(request):
    pagos = Pago.objects.all()
    return render(request, 'pagos/lista_pagos.html', {'pagos': pagos})


@login_required
def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('lista_pagos')
    else:
        form = PagoForm()
    return render(request, 'pagos/registrar_pago.html', {'form': form})


@login_required
def editar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago actualizado correctamente.')
            return redirect('lista_pagos')
    else:
        form = PagoForm(instance=pago)
    return render(request, 'pagos/editar_pago.html', {'form': form})


@login_required
def eliminar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    pago.delete()
    messages.success(request, 'Pago eliminado correctamente.')
    return redirect('lista_pagos')

# Exportar datos a Excel

@login_required
@user_passes_test(es_admin)
def exportar_excel(request):
    dueños = Dueño.objects.all().values()
    vehiculos = Vehiculo.objects.all().values()
    trabajadores = Trabajador.objects.all().values()
    reparaciones = Reparacion.objects.all().values()

    # Crear un DataFrame para cada modelo
    df_dueños = pd.DataFrame(list(dueños))
    df_vehiculos = pd.DataFrame(list(vehiculos))
    df_trabajadores = pd.DataFrame(list(trabajadores))
    df_reparaciones = pd.DataFrame(list(reparaciones))

    # Crear un archivo Excel con pandas
    with pd.ExcelWriter('historial_empresa.xlsx', engine='openpyxl') as writer:
        df_dueños.to_excel(writer, sheet_name='Dueños', index=False)
        df_vehiculos.to_excel(writer, sheet_name='Vehículos', index=False)
        df_trabajadores.to_excel(
            writer, sheet_name='Trabajadores', index=False)
        df_reparaciones.to_excel(
            writer, sheet_name='Reparaciones', index=False)

    # Configurar la respuesta HTTP para descargar el archivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="historial_empresa.xlsx"'

    # Guardar el archivo Excel
    writer.save()
    return response
