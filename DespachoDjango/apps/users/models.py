import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """Gestor personalizado para el modelo de usuario."""

    def _create_user(self, email, password, **extra_fields):
        """
        Crea y guarda un usuario con el email y contraseña dados.
        """
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Crear perfil automáticamente según el rol
        if user.role == User.Roles.OWNER:
            DuenoProfile.objects.create(user=user)
        elif user.role == User.Roles.WORKER:
            TrabajadorProfile.objects.create(user=user)
        elif user.role == User.Roles.SUPERVISOR:
            SupervisorProfile.objects.create(user=user)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """Crea un usuario normal."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        """Crea un superusuario."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Cambiado de 'admin'
        extra_fields.setdefault('role', User.Roles.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo de usuario personalizado que usa email como identificador principal"""

    class Roles(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        OWNER = 'owner', 'Dueño'
        WORKER = 'worker', 'Trabajador'
        SUPERVISOR = 'supervisor', 'Supervisor'

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )

    # Campos básicos
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField('Correo Electrónico', unique=True)
    nombre = models.CharField('Nombre', max_length=150, default="Usuario")
    apellido = models.CharField(
        'Apellido', max_length=150, default="Sin Apellido")
    telefono = models.CharField(
        'Teléfono',
        validators=[phone_regex],
        max_length=17,
        blank=True
    )
    direccion = models.TextField('Dirección', blank=True)
    role = models.CharField(
        'Rol',
        max_length=20,
        choices=Roles.choices,
        default=Roles.OWNER
    )
    avatar = models.ImageField(
        'Foto de Perfil',
        upload_to='avatars/%Y/%m/',
        null=True,
        blank=True
    )

    # Campos de estado
    is_active = models.BooleanField('Activo', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Superusuario', default=False)
    date_joined = models.DateTimeField(
        'Fecha de Registro', default=timezone.now)
    last_login = models.DateTimeField('Último Acceso', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']

    def get_full_name(self):
        """Retorna el nombre completo del usuario."""
        return f"{self.nombre} {self.apellido}".strip()

    def get_short_name(self):
        """Retorna el nombre corto del usuario."""
        return self.nombre

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Envía un email al usuario"""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_owner(self):
        return self.role == self.Roles.OWNER

    @property
    def is_worker(self):
        return self.role == self.Roles.WORKER

    @property
    def is_supervisor(self):
        return self.role == self.Roles.SUPERVISOR


class DuenoProfile(models.Model):
    """Perfil extendido para usuarios con rol de dueño (dueños de vehículos)"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='dueno_profile'
    )
    rut = models.CharField('RUT', max_length=20, unique=True)
    direccion = models.CharField('Dirección', max_length=255)
    telefono_contacto = models.CharField('Teléfono de Contacto', max_length=17)
    historial_vehiculos = models.JSONField(
        'Historial de Vehículos',
        default=dict,
        blank=True
    )
    fecha_registro = models.DateTimeField(
        'Fecha de Registro',
        auto_now_add=True
    )
    total_gastado = models.DecimalField(
        'Total Gastado en Reparaciones',
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'dueno_profiles'
        verbose_name = 'Perfil de Dueño'
        verbose_name_plural = 'Perfiles de Dueños'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"


class TrabajadorProfile(models.Model):
    """Perfil extendido para usuarios con rol de trabajador"""

    TIPO_LICENCIA_CHOICES = [
        ('A', 'Clase A'),
        ('B', 'Clase B'),
        ('C', 'Clase C'),
        ('D', 'Clase D'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='trabajador_profile'
    )
    licencia = models.CharField(
        'Licencia',
        max_length=50,
        choices=TIPO_LICENCIA_CHOICES
    )
    numero_licencia = models.CharField(
        'Número de Licencia',
        max_length=20,
        unique=True
    )
    especialidad = models.CharField('Especialidad', max_length=100)
    disponibilidad = models.BooleanField('Disponible', default=True)
    trabajos_completados = models.PositiveIntegerField(
        'Trabajos Completados',
        default=0
    )
    calificacion_promedio = models.DecimalField(
        'Calificación Promedio',
        max_digits=3,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'trabajador_profiles'
        verbose_name = 'Perfil de Trabajador'
        verbose_name_plural = 'Perfiles de Trabajadores'

    def __str__(self):
        return f"Trabajador: {self.user.get_full_name()}"

    def actualizar_calificacion(self, nueva_calificacion):
        """Actualiza la calificación promedio del trabajador."""
        self.calificacion_promedio = (
            (self.calificacion_promedio * self.trabajos_completados + nueva_calificacion) /
            (self.trabajos_completados + 1)
        )
        self.trabajos_completados += 1
        self.save()


class SupervisorProfile(models.Model):
    """Perfil extendido para usuarios con rol de supervisor"""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='supervisor_profile'
    )
    departamento = models.CharField('Departamento', max_length=100)
    cargo = models.CharField('Cargo', max_length=100)
    fecha_contratacion = models.DateField(
        'Fecha de Contratación', default=timezone.now)
    supervisados = models.ManyToManyField(
        TrabajadorProfile,
        related_name='supervisor',
        blank=True
    )

    class Meta:
        db_table = 'supervisor_profiles'
        verbose_name = 'Perfil de Supervisor'
        verbose_name_plural = 'Perfiles de Supervisores'

    def __str__(self):
        return f"Supervisor: {self.user.get_full_name()}"
