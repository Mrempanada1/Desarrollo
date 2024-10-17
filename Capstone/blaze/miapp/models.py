from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from datetime import datetime


# Usuarios
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        # Verifica si el usuario tiene permisos sobre un modulo
        return True


# Perfiles de ingreso
class Perfil(models.Model):
    ROLE_CHOICES = (
        ('dueño', 'Dueño'),
        ('trabajador', 'Trabajador'),
        ('administrador', 'Administrador'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    rol = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='dueño')


    def __str__(self):
        return f"{self.user.email} - {self.rol}"


# Crear el perfil automáticamente
@receiver(post_save, sender=CustomUser)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()


class Dueño(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Vehiculo(models.Model):
    patente = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.IntegerField()

    def clean(self):
        if self.año < 1886 or self.año > datetime.now().year:
            raise ValidationError(_('Año inválido para el vehículo.'))

    color = models.CharField(max_length=50)
    kilometraje = models.IntegerField()
    tipo_combustible = models.CharField(max_length=50)
    fecha_ultima_revision = models.DateField()
    estado_vehiculo = models.CharField(max_length=100, choices=[
        ('disponible', 'Disponible'),
        ('en_reparacion', 'En Reparación'),
        ('no_disponible', 'No Disponible'),
    ])
    dueño = models.ForeignKey(Dueño, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('patente', 'dueño')

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente}) - Estado: {self.estado_vehiculo}"


class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.IntegerField()
    garantia = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_servicio


class Trabajador(models.Model):
    id_trabajador = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField()
    disponibilidad = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)
    asignacion = models.CharField(max_length=50)
    perfil = models.ForeignKey(
        Perfil, on_delete=models.CASCADE, related_name='trabajadores')

    # Rol
    rol = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol}"


class Proceso(models.Model):
    fase_proceso = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado_proceso = models.CharField(max_length=100)
    prioridad = models.CharField(max_length=50)
    comentarios = models.TextField(null=True, blank=True)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    notificaciones = models.ForeignKey(
        'Notificacion', on_delete=models.CASCADE, related_name='procesos_relacionados', null=True)

    def __str__(self):
        return f"{self.fase_proceso} - {self.estado_proceso}"


class Notificacion(models.Model):
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50)
    proceso = models.ForeignKey(
        'Proceso', on_delete=models.CASCADE, related_name='notificaciones_proceso')

    def __str__(self):
        return f"Notificación {self.id} - Estado: {self.estado}"


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=100)
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pago {self.id} - {self.estado_pago}"


class Cita(models.Model):
    fecha_y_hora = models.DateTimeField()
    motivo = models.TextField()
    estado_cita = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cita {self.id} - {self.estado_cita}"


class Cotizacion(models.Model):
    ESTADO_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    estado = models.CharField(
        max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    total_estimado = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)  # Nuevo campo
    monto_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)  # Nuevo campo

    def __str__(self):
        return f"Cotización {self.id} - {self.estado}"

    def calcular_total_estimado(self):
        total = sum(
            detalle.costo_servicio for detalle in self.detalles.all())
        self.total_estimado = total
        self.save()


class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(
        Cotizacion, on_delete=models.CASCADE, related_name='detalles')
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    costo_servicio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cotizacion} - {self.servicio.nombre_servicio}"
