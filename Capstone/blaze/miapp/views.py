# Importaciones de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

# Importaciones de la aplicación
from .models import Dueño, Vehiculo, Trabajador, Cita, Pago, Servicio, Proceso, Perfil, Cotizacion, DetalleCotizacion, CustomUser, Notificacion
from .forms import DueñoForm, VehiculoForm, TrabajadorForm, CitaForm, ServicioForm, PagoForm, ProcesoForm, UserRegistrationForm, CotizacionForm, DetalleCotizacion, NotificacionForm

# Librerias
import pandas as pd
from openpyxl import Workbook


# Perfiles


def perfil_requerido(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not (hasattr(request.user, 'dueño') or hasattr(request.user, 'trabajador') or hasattr(request.user, 'administrador')):
            return HttpResponseForbidden('No tienes permiso para ver esta página.')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            Perfil.objects.create(user=instance, rol='Admin')
        else:
            Perfil.objects.create(user=instance, rol='Dueño')


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
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {user.first_name}!")

            # Redirección según el rol del usuario
            if user.perfil.rol == 'Admin':
                return redirect('inicio')
            elif user.perfil.rol == 'Dueño':
                return redirect('inicio')
            else:
                return redirect('inicio')
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
    return render(request, 'login.html')


# Vista para la creacion de trabajadores (solo accesible por administradores)


# @ login_required
# @user_passes_test(es_admin)
def crear_trabajador(request):
    if request.user.perfil.rol != 'Admin':
        messages.error(
            request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')  # Redirigir a la vista de inicio

    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            trabajador = form.save(commit=False)
            # Crear usuario y asignar el perfil correspondiente
            email = form.cleaned_data['email']
            # Asegúrate de tener este campo en tu formulario
            password = form.cleaned_data['password']
            user = CustomUser.objects.create_user(
                email=email, password=password)
            trabajador.perfil = Perfil.objects.create(
                user=user, rol='Trabajador')
            trabajador.save()
            messages.success(request, 'Trabajador creado con éxito.')
            return redirect('home')
    else:
        form = TrabajadorForm()
    return render(request, 'trabajadores/crear_trabajador.html', {'form': form})

# Vista para gestionar la lista de trabajadores (solo accesible por administradores)


# @ login_required
def lista_trabajadores(request):
    if request.user.perfil.rol != 'Admin':
        messages.error(
            request, 'No tienes permiso para acceder a esta página.')
        return redirect('home')  # Redirigir a la vista de inicio

    trabajadores = Trabajador.objects.all()
    return render(request, 'trabajadores/lista_trabajadores.html', {'trabajadores': trabajadores})

# Mi cuenta


# @ login_required
def mi_cuenta(request):
    user = request.user

    # Obtener los vehuculos asociados al dueño si el usuario tiene el rol de dueño
    vehiculos = Vehiculo.objects.filter(
        dueño=user.perfil) if user.perfil.rol == 'dueño' else None

    # Obtener los procesos asociados al trabajador o dueño segun el rol del usuario
    if user.perfil.rol == 'dueño':
        procesos = Proceso.objects.filter(vehiculo__dueño=user.perfil)
    elif user.perfil.rol == 'trabajador':
        procesos = Proceso.objects.filter(trabajador=user.perfil)
    else:
        procesos = Proceso.objects.all()

    # Obtener los pagos asociados al dueño si el usuario tiene el rol de dueño
    pagos = Pago.objects.filter(
        reparacion__vehiculo__dueño=user.perfil) if user.perfil.rol == 'dueño' else None

    context = {
        'user': user,
        'vehiculos': vehiculos,
        'procesos': procesos,
        'pagos': pagos,
    }

    return render(request, 'mi_cuenta.html', context)


# Usuario

CustomUser = get_user_model()


def registrar_usuario(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=form.cleaned_data['password']
            )
            # Verificar si ya existe un perfil para el usuario
            perfil, created = Perfil.objects.get_or_create(user=user)
            if created:
                user.save()
                perfil = Perfil(user=user, rol='Cliente')
                perfil.save()
                messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('inicio')
    else:
        form = UserRegistrationForm()

    return render(request, 'registrar_usuario.html', {'form': form})

# Gestión de Clientes


# @ login_required
def lista_dueños(request):
    dueños = Dueño.objects.all()
    return render(request, 'dueños/lista_dueños.html', {'dueños': dueños})


# @ login_required
def registrar_dueño(request):
    if request.method == 'POST':
        form = DueñoForm(request.POST)
        if form.is_valid():
            dueño = form.save(commit=False)
            dueño.user = request.user
            dueño.save()
            messages.success(request, 'Dueño registrado correctamente.')
            return redirect('inicio')
        else:
            messages.error(
                request, 'Por favor corrige los errores en el formulario.')
    else:
        form = DueñoForm()

    return render(request, 'dueños/registrar_dueño.html', {'form': form})


# @ login_required
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


# @ login_required
# @ user_passes_test(es_admin)
def eliminar_dueño(request, dueño_id):
    dueño = get_object_or_404(Dueño, id=dueño_id)
    dueño.delete()
    messages.success(request, 'Dueño eliminado correctamente.')
    return redirect(reverse('dueños/lista_dueños'))

# Gestión de Vehículos


# @ login_required
def lista_vehiculos(request):
    try:
        # Intentar obtener el dueño del usuario autenticado
        dueño = request.user.dueño
    except ObjectDoesNotExist:
        # Si el usuario no tiene un dueño asociado mostrar un mensaje de error
        messages.error(request, "El usuario no tiene un dueño asociado.")
        # Redirige a otra vista
        return redirect('inicio')

    # Si tiene un dueño, obtener los vehiculos asociados
    vehiculos = Vehiculo.objects.filter(dueño=dueño)

    # Crear un diccionario que asocie cada vehiculo con sus procesos
    vehiculos_procesos = []
    for vehiculo in vehiculos:
        # Obtener los procesos asociados a cada vehiculo
        procesos = Proceso.objects.filter(vehiculo=vehiculo)
        vehiculos_procesos.append({
            'vehiculo': vehiculo,
            'procesos': procesos
        })

    return render(request, 'vehiculos/lista_vehiculos.html', {
        'vehiculos_procesos': vehiculos_procesos
    })


# @ login_required
def registrar_vehiculo(request):
    if not hasattr(request.user, 'dueño'):
        messages.error(request, 'No tienes un perfil de dueño asociado.')
        return redirect('inicio')

    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.dueño = request.user.dueño  # Asignar el dueño que ha iniciado sesion
            vehiculo.save()
            messages.success(request, 'Vehículo registrado correctamente.')
            return redirect('lista_vehiculos')
    else:
        form = VehiculoForm()

    return render(request, 'vehiculos/registrar_vehiculo.html', {'form': form})


# @ login_required
def editar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado correctamente.')
            return redirect('inicio')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiculos/editar_vehiculo.html', {'form': form})

# Gestión de Reparaciones


# @ login_required
def lista_procesos(request):
    procesos = Proceso.objects.all()
    return render(request, 'procesos/lista_procesos.html', {'procesos': procesos})

# Registrar proceso asociado a una reparación (solo accesible por administradores)


# @ login_required
# @ user_passes_test(es_admin)
def registrar_proceso(request):
    if request.method == 'POST':
        form = ProcesoForm(request.POST)
        if form.is_valid():
            proceso = form.save(commit=False)
            proceso.save()  # Guardar el proceso
            messages.success(request, 'Proceso registrado correctamente.')
            return redirect('lista_procesos')
    else:
        form = ProcesoForm()
    return render(request, 'procesos/registrar_proceso.html', {'form': form})

# Editar proceso de reparación


# @ login_required
# @ user_passes_test(es_admin)
def editar_proceso(request, pk):
    proceso = get_object_or_404(Proceso, pk=pk)
    if request.method == 'POST':
        form = ProcesoForm(request.POST, instance=proceso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proceso actualizado correctamente.')
            return redirect('lista_procesos')
    else:
        form = ProcesoForm(instance=proceso)
    return render(request, 'procesos/editar_proceso.html', {'form': form})

# Eliminar proceso


# @ login_required
# @ user_passes_test(es_admin)
def eliminar_proceso(request, pk):
    proceso = get_object_or_404(Proceso, pk=pk)
    proceso.delete()
    messages.success(request, 'Proceso eliminado correctamente.')
    return redirect('lista_procesos')


# Gestión de Citas


# @ login_required
def lista_citas(request):
    citas = Cita.objects.all()
    return render(request, 'citas/lista_citas.html', {'citas': citas})


# @ login_required
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


# @ login_required
def registrar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_citas')
    else:
        form = CitaForm()
    return render(request, 'citas/registrar_cita.html', {'form': form})


# @ login_required
def eliminar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    cita.delete()
    messages.success(request, 'Cita eliminada correctamente.')
    return redirect('lista_citas')

# Gestión de Pagos


# @ login_required
def lista_pagos(request):
    pagos = Pago.objects.all()
    return render(request, 'pagos/lista_pagos.html', {'pagos': pagos})


# @ login_required
def registrar_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            # Asignar el proceso en lugar de reparación
            pago.proceso = form.cleaned_data['proceso']
            pago.save()
            messages.success(request, 'Pago registrado correctamente.')
            return redirect('lista_pagos')
    else:
        form = PagoForm()
    return render(request, 'pagos/registrar_pago.html', {'form': form})


# @ login_required
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

# Gestión de Cotizaciones


# @ login_required
def lista_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all()
    return render(request, 'cotizaciones/lista_cotizaciones.html', {'cotizaciones': cotizaciones})


# @ login_required
def registrar_cotizacion(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cotización registrada correctamente.')
            return redirect('lista_cotizaciones')
    else:
        form = CotizacionForm()
    return render(request, 'cotizaciones/registrar_cotizacion.html', {'form': form})


# @ login_required
def editar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == 'POST':
        form = CotizacionForm(request.POST, instance=cotizacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cotización actualizada correctamente.')
            return redirect('lista_cotizaciones')
    else:
        form = CotizacionForm(instance=cotizacion)
    return render(request, 'cotizaciones/editar_cotizacion.html', {'form': form})


# @ login_required
# @ user_passes_test(es_admin)
def eliminar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    cotizacion.delete()
    messages.success(request, 'Cotización eliminada correctamente.')
    return redirect('lista_cotizaciones')

# Exportar a Excel


# @ login_required
# @ user_passes_test(es_admin)
def exportar_datos(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Datos de Procesos"

    ws.append(['ID', 'Fase de Proceso', 'Descripción', 'Fecha de Inicio',
               'Fecha de Fin', 'Estado', 'Prioridad'])

    procesos = Proceso.objects.all()
    for proceso in procesos:
        ws.append([proceso.id, proceso.fase_proceso, proceso.descripcion, proceso.fecha_inicio,
                   proceso.fecha_fin, proceso.estado_proceso, proceso.prioridad])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=procesos.xlsx'
    wb.save(response)
    return response

# Vista para mostrar los datos


# @ login_required
# @ user_passes_test(es_admin)
def mostrar_procesos(request):
    procesos = Proceso.objects.all()  # Obtener todos los procesos
    return render(request, 'exportar_datos.html', {'procesos': procesos})
