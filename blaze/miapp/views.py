from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import VehiculoForm
from .models import Vehiculo
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def inicio(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect('panel')
        else:
            messages.error(
                request, "Datos incorrectos. Intenta nuevamente.")
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión después de registrarse
            return redirect('registro_vehiculo')
    else:
        form = UserCreationForm()
    return render(request, 'registro_clientes.html', {'form': form})


def registrar_vehiculo(request):
    # Obtener el año actual
    current_year = timezone.now().year

    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.cliente = request.user  # Esto asocia el vehículo al cliente
            vehiculo.save()
            messages.success(request, "Vehículo registrado exitosamente.")
            return redirect('lista_vehiculos')
    else:
        form = VehiculoForm()

    return render(request, 'registro_vehiculo.html', {'form': form, 'current_year': current_year})


def lista_vehiculos(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirige al login si no está autenticado

    vehiculos = Vehiculo.objects.filter(cliente=request.user)
    return render(request, 'lista_vehiculos.html', {'vehiculos': vehiculos})
