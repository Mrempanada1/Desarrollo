from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'miapp':
        groups = [
            'Clientes',
            'Administradores'
        ]
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)

            # Asignar permisos (ejemplo para los grupos)
            if group_name == 'Administradores':
                permissions = Permission.objects.all()  # Asignar todos los permisos
                group.permissions.set(permissions)
            elif group_name == 'Clientes':
                permissions = Permission.objects.all()  # Asignar todos los permisos
                group.permissions.set(permissions)
                pass
