from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MiappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'miapp'
    verbose_name = "Gestión de Talleres Automotrices"

    def ready(self):
        # Conectar la señal post_migrate al cargar la aplicación
        post_migrate.connect(create_groups, sender=self)


def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission  # Mover la importación aquí
    from django.contrib.contenttypes.models import ContentType
    from miapp.models import Vehiculo, Proceso, Cotizacion, Cita, Pago, Trabajador, Dueño

    # Definir los grupos y permisos
    groups = {
        'Clientes': {
            'models': [Vehiculo, Proceso, Cotizacion, Cita, Pago],
            'actions': ['view', 'add'],  # Consultar y registrar
        },
        'Administradores': {
            'models': [Trabajador, Dueño, Proceso, Pago, Cotizacion, Cita],
            # Consultar, registrar, modificar y eliminar
            'actions': ['view', 'add', 'change', 'delete'],
        },
        'Trabajadores': {
            'models': [Proceso],
            'actions': ['view', 'add'],  # Consultar y registrar procesos
        }
    }

    for group_name, permissions_data in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        for model in permissions_data['models']:
            content_type = ContentType.objects.get_for_model(model)
            for action in permissions_data['actions']:
                permission = Permission.objects.get(
                    codename=f'{action}_{model._meta.model_name}',
                    content_type=content_type
                )
                group.permissions.add(permission)
