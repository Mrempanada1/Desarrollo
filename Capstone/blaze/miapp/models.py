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
        return f"{self.user.username} - {self.get_rol_display()}"


class Dueño(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    # Relación con el Dueño
    dueño = models.ForeignKey(Dueño, on_delete=models.CASCADE)

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
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE)  # Relación con Vehículo

    def __str__(self):
        return f"Reparación {self.id} - {self.estado_reparacion}"

    @property
    def costo_total(self):
        return sum(servicio.costo for servicio in self.servicio_set.all())


class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=100)
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.DurationField()
    garantia = models.CharField(max_length=100)
    reparacion = models.ForeignKey(
        Reparacion, on_delete=models.CASCADE)  # Relación con Reparación

    def __str__(self):
        return self.nombre_servicio


class Trabajador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    # Puede ser mecanico, pintor, etc.
    asignacion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    disponibilidad = models.BooleanField(
        default=True)  # Disponible para asignaciones
    estado = models.CharField(max_length=50)  # Estado laboral del trabajador

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
    trabajador = models.ForeignKey(
        Trabajador, on_delete=models.CASCADE)  # Relación con Trabajador

    def __str__(self):
        return f"{self.fase_proceso} - {self.estado_proceso}"


class Pago(models.Model):
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado_pago = models.CharField(max_length=100)
    reparacion = models.ForeignKey(
        Reparacion, on_delete=models.CASCADE)  # Relación con Reparación

    def __str__(self):
        return f"Pago {self.id} - {self.estado_pago}"


class Cita(models.Model):
    fecha_y_hora = models.DateTimeField()
    motivo = models.TextField()
    estado_cita = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE)  # Relación con Vehículo

    def __str__(self):
        return f"Cita {self.id} - {self.estado_cita}"


class Cotizacion(models.Model):
    # Fecha de creación de la cotización
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE)  # Relación con Vehículo
    # Estado: Pendiente, Aceptada, Rechazada
    estado = models.CharField(max_length=100, default='Pendiente')
    total_estimado = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)  # Total estimado

    def __str__(self):
        return f"Cotización {self.id} - {self.estado}"

    @property
    def calcular_total_estimado(self):
        """
        Método para calcular el total estimado de la cotización en base a los servicios asociados.
        """
        total = sum(
            item.costo_servicio for item in self.detallecotizacion_set.all())
        self.total_estimado = total
        self.save()  # Guardar el valor del total estimado
        return total


class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(
        Cotizacion, on_delete=models.CASCADE)  # Relación con Cotización
    servicio = models.ForeignKey(
        Servicio, on_delete=models.CASCADE)  # Relación con Servicio
    # Costo del servicio en la cotización
    costo_servicio = models.DecimalField(max_digits=10, decimal_places=2)
    # Descripción adicional si es necesario
    descripcion_adicional = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.servicio.nombre_servicio} - {self.costo_servicio}"


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

    def __str__(self):
        return f"Cotización {self.id} - {self.estado}"

    @property
    def calcular_total_estimado(self):
        total = sum(
            item.costo_servicio for item in self.detallecotizacion_set.all())
        self.total_estimado = total
        self.save()
        return total
