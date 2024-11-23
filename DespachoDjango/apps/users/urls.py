from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'users'

urlpatterns = [
    # Redirección de /accounts/ a home
    path('', RedirectView.as_view(pattern_name='home:home'), name='users_home'),

    # Dueños
    path('dueños/', views.UserListView.as_view(
        extra_context={'user_type': 'dueños', 'title': 'Dueños'}
    ), name='dueño_list'),
    path('dueños/create/', views.UserCreateView.as_view(
        extra_context={'user_type': 'dueño', 'title': 'Nuevo Dueño'}
    ), name='create_dueño'),

    # Trabajadores
    path('trabajadores/', views.UserListView.as_view(
        extra_context={'user_type': 'trabajadores', 'title': 'Trabajadores'}
    ), name='trabajador_list'),
    path('trabajadores/create/', views.UserCreateView.as_view(
        extra_context={'user_type': 'trabajador', 'title': 'Nuevo Trabajador'}
    ), name='create_trabajador'),

    # Supervisores
    path('supervisores/', views.UserListView.as_view(
        extra_context={'user_type': 'supervisores', 'title': 'Supervisores'}
    ), name='supervisor_list'),
    path('supervisores/create/', views.UserCreateView.as_view(
        extra_context={'user_type': 'supervisor', 'title': 'Nuevo Supervisor'}
    ), name='create_supervisor'),

    # Operaciones comunes
    path('dueños/<uuid:pk>/update/', views.UserUpdateView.as_view(
        extra_context={'user_type': 'dueño'}
    ), name='update_dueño'),
    path('trabajadores/<uuid:pk>/update/', views.UserUpdateView.as_view(
        extra_context={'user_type': 'trabajador'}
    ), name='update_trabajador'),
    path('supervisores/<uuid:pk>/update/', views.UserUpdateView.as_view(
        extra_context={'user_type': 'supervisor'}
    ), name='update_supervisor'),

    path('dueños/<uuid:pk>/detail/', views.UserDetailView.as_view(
        extra_context={'user_type': 'dueño'}
    ), name='detail_dueño'),
    path('trabajadores/<uuid:pk>/detail/', views.UserDetailView.as_view(
        extra_context={'user_type': 'trabajador'}
    ), name='detail_trabajador'),
    path('supervisores/<uuid:pk>/detail/', views.UserDetailView.as_view(
        extra_context={'user_type': 'supervisor'}
    ), name='detail_supervisor'),
]
