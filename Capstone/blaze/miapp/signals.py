from django.db.models.signals import post_migrate, post_save, post_delete
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from .models import DetalleCotizacion


@receiver(post_save, sender=DetalleCotizacion)
def actualizar_total_estimado(sender, instance, **kwargs):
    instance.cotizacion.calcular_total_estimado()


@receiver(post_delete, sender=DetalleCotizacion)
def actualizar_total_estimado_on_delete(sender, instance, **kwargs):
    instance.cotizacion.calcular_total_estimado()


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
