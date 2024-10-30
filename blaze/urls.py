"""
URL configuration for blaze project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from miapp import views
from django.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Gestion de usuarios
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('mi-cuenta/', views.mi_cuenta, name='mi_cuenta'),
    path('registrar-usuario/', views.registrar_usuario, name='registrar_usuario'),

    # Gestion de vehiculos
    path('vehiculos/registrar/', views.registrar_vehiculo,
         name='registro_vehiculo'),
    path('vehiculos/', views.lista_vehiculos, name='lista_vehiculos'),
    path('vehiculos/editar/<int:pk>/',
         views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:pk>/',
         views.eliminar_vehiculo, name='eliminar_vehiculo'),

    # Gestion de dueños
    path('dueños/registrar/', views.registrar_dueño, name='registro_dueño'),
    path('dueños/', views.lista_dueños, name='lista_dueños'),
    path('dueños/editar/<int:id>/', views.editar_dueño, name='editar_dueño'),
    path('dueños/eliminar/<int:dueño_id>/',
         views.eliminar_dueño, name='eliminar_dueño'),

    # Gestion de trabajadores
    path('trabajadores/', views.lista_trabajadores, name='lista_trabajadores'),
    path('trabajadores/crear/', views.crear_trabajador, name='crear_trabajador'),
    path('trabajadores/editar/<int:id_trabajador>/',
         views.editar_trabajador, name='editar_trabajador'),
    path('trabajadores/eliminar/<int:id_trabajador>/',
         views.eliminar_trabajador, name='eliminar_trabajador'),

    # Gestion de citas
    path('citas/registrar/', views.registrar_cita, name='registro_cita'),
    path('citas/', views.lista_citas, name='lista_citas'),
    path('citas/editar/<int:pk>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:pk>/', views.eliminar_cita, name='eliminar_cita'),

    # Gestion de pagos
    path('pagos/registrar/', views.registrar_pago, name='registro_pago'),
    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/editar/<int:pk>/', views.editar_pago, name='editar_pago'),

    # Gestion procesos
    path('procesos/registrar/', views.registrar_proceso,
         name='registro_proceso'),
    path('procesos/', views.lista_procesos, name='lista_procesos'),
    path('procesos/editar/<int:pk>/',
         views.editar_proceso, name='editar_proceso'),
    path('procesos/eliminar/<int:pk>/',
         views.eliminar_proceso, name='eliminar_proceso'),

    # Gestion de cotizaciones
    path('cotizaciones/registrar/', views.registrar_cotizacion,
         name='registrar_cotizacion'),
    path('cotizaciones/', views.lista_cotizaciones, name='lista_cotizaciones'),
    path('cotizaciones/editar/<int:pk>/',
         views.editar_cotizacion, name='editar_cotizacion'),
    path('cotizaciones/eliminar/<int:pk>/',
         views.eliminar_cotizacion, name='eliminar_cotizacion'),

    # Ruta para mostrar los datos de procesos
    path('procesos/', views.mostrar_procesos, name='mostrar_procesos'),

    # Ruta para exportar los datos a Excel
    path('exportar-datos/', views.exportar_datos, name='exportar_datos'),

]
