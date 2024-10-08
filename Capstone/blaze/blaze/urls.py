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
    path('vehiculos/', include([
        path('registrar/', views.registrar_vehiculo, name='registro_vehiculo'),
        path('', views.lista_vehiculos, name='lista_vehiculos'),
        path('editar/<int:id>/', views.editar_vehiculo, name='editar_vehiculo'),
    ])),

    # Gestion de dueños
    path('dueños/', include([
        path('registrar/', views.registrar_dueño, name='registro_dueño'),
        path('', views.lista_dueños, name='lista_dueños'),
        path('editar/<int:id>/', views.editar_dueño, name='editar_dueño'),
        path('eliminar/<int:pk>/', views.eliminar_dueño, name='eliminar_dueño'),
    ])),

    # Gestion de citas
    path('citas/', include([
        path('registrar/', views.registrar_cita, name='registro_cita'),
        path('', views.lista_citas, name='lista_citas'),
        path('editar/<int:id>/', views.editar_cita, name='editar_cita'),
    ])),

    # Gestion de pagos
    path('pagos/', include([
        path('registrar/', views.registrar_pago, name='registro_pago'),
        path('', views.lista_pagos, name='lista_pagos'),
        path('editar/<int:id>/', views.editar_pago, name='editar_pago'),
    ])),

    # Gestion reparaciones
    path('reparaciones/', include([
        path('registrar/', views.registrar_reparacion,
             name='registro_reparacion'),
        path('', views.lista_reparaciones, name='lista_reparaciones'),
        path('editar/<int:id>/', views.editar_reparacion,
             name='editar_reparacion'),
    ])),
]
