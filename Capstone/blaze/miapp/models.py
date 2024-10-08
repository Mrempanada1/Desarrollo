from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    ROLE_CHOICES = (
        ('dueño', 'Dueño'),
        ('trabajador', 'Trabajador'),
        ('administrador', 'Administrador'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username


class Dueño(models.Model):
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
    color = models.CharField(max_length=50)
    kilometraje = models.IntegerField()
    tipo_combustible = models.CharField(max_length=50)
    fecha_ultima_revision = models.DateField()
    estado_vehiculo = models.CharField(max_length=100)
    dueño = models.ForeignKey(Dueño, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.patente})"


class Reparacion(models.Model):
    desc_problema = models.TextField()
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_estimada_fin = models.DateTimeField()
    estado_reparacion = models.CharField(max_length=100)
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    costo_final = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Reparación {self.id} - {self.estado_reparacion}"

    # Costo total de una reparacion sumando todos los costos de los servicios asociados
    # Puede ser una opcion

    @property
    def costo_total(self):
        return sum(servicio.costo for servicio in self.servicio_set.all())


class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.DurationField()
    garantia = models.CharField(max_length=100)
    reparacion = models.ForeignKey(Reparacion, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_servicio


class Trabajador(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    asignacion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    disponibilidad = models.BooleanField(default=True)
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Proceso(models.Model):
    fase_proceso = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado_proceso = models.CharField(max_length=100)
    prioridad = models.CharField(max_length=50)
    comentarios = models.TextField(null=True, blank=True)
    notificaciones_id_notificacion = models.IntegerField()
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fase_proceso} - {self.estado_proceso}"


class Pago(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=100)
    reparacion = models.ForeignKey(Reparacion, on_delete=models.CASCADE)

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
