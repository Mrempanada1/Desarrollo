import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

# Modelo de cotización


class Cotizacion(models.Model):
    """Modelo que representa una cotización en el sistema."""

    class MetodoPago(models.TextChoices):
        EFECTIVO = 'efectivo', 'Efectivo'
        TARJETA = 'tarjeta', 'Tarjeta'
        TRANSFERENCIA = 'transferencia', 'Transferencia'
        OTRO = 'otro', 'Otro'

    # Campos de identificación
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_cotizacion = models.CharField(
        'Número de Cotización',
        max_length=10,
        unique=True,
        editable=False
    )

    # Campos de dueño
    dueño = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cotizaciones',
        limit_choices_to={'role': 'owner'},
        verbose_name='Dueño',
        null=True,
        blank=True
    )
    rut_dueño = models.CharField(
        'RUT DUEÑO',
        max_length=12,
        blank=True
    )

    # Campos de pago
    metodo_pago = models.CharField(
        'Método de Pago',
        max_length=20,
        choices=MetodoPago.choices,
        default=MetodoPago.EFECTIVO
    )
    subtotal = models.IntegerField(
        'Subtotal',
        default=0,
        validators=[MinValueValidator(0)]
    )
    impuestos = models.IntegerField(
        'Impuestos',
        default=0,
        validators=[MinValueValidator(0)]
    )
    total = models.IntegerField(
        'Total',
        default=0,
        validators=[MinValueValidator(0)]
    )

    # Campos de estado y seguimiento
    estado = models.CharField(
        'Estado',
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('aprobada',
                                              'Aprobada'), ('rechazada', 'Rechazada')],
        default='pendiente'
    )
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='cotizaciones_realizadas',
        limit_choices_to={'is_staff': True},
        verbose_name='Supervisor'
    )
    notas = models.TextField('Notas', blank=True)

    # Campos de fecha
    fecha_cotizacion = models.DateTimeField(
        'Fecha de Cotización', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(
        'Última Actualización', auto_now=True)

    class Meta:
        db_table = 'cotizaciones'
        verbose_name = 'Cotización'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['-fecha_cotizacion']

    def __str__(self):
        return f'Cotización {self.numero_cotizacion} - {self.cliente.get_full_name()}'

    def save(self, *args, **kwargs):
        """Genera número de cotización y calcula totales antes de guardar"""
        if not self.numero_cotizacion:
            last_cotizacion = Cotizacion.objects.order_by('-id').first()
            if last_cotizacion:
                self.numero_cotizacion = f'CTZ{
                    str(last_cotizacion.id + 1).zfill(6)}'
            else:
                self.numero_cotizacion = 'CTZ000001'

        self.subtotal = sum(
            detalle.costo_servicio for detalle in self.detalles.all())
        self.impuestos = self.subtotal * 19 // 100  # 19% IVA de prueba
        self.total = self.subtotal + self.impuestos

        super().save(*args, **kwargs)


# Modelo de detalle de cotización
class DetalleCotizacion(models.Model):
    """Modelo que representa el detalle de una cotización"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cotizacion = models.ForeignKey(
        Cotizacion,
        related_name='detalles',
        on_delete=models.CASCADE,
        verbose_name='Cotización'
    )
    servicio = models.ForeignKey(
        'Servicio',  # Asegúrate de que el modelo 'Servicio' exista
        on_delete=models.PROTECT,
        related_name='cotizaciones',
        verbose_name='Servicio'
    )
    costo_servicio = models.IntegerField(
        'Costo del Servicio',
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        db_table = 'detalles_cotizacion'
        verbose_name = 'Detalle de Cotización'
        verbose_name_plural = 'Detalles de Cotización'

    def __str__(self):
        return f'{self.servicio.nombre_servicio} - {self.costo_servicio}'

    def save(self, *args, **kwargs):
        """Calcula el costo del servicio antes de guardar."""
        # Si el costo no es asignado manualmente, toma el costo por defecto del servicio
        if not self.costo_servicio:
            self.costo_servicio = self.servicio.costo

        super().save(*args, **kwargs)
        # Actualiza totales de la cotización
        self.cotizacion.save()


# Modelo de servicio
class Servicio(models.Model):
    """Modelo que representa un servicio disponible para cotizar."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_servicio = models.CharField('Nombre del Servicio', max_length=255)
    descripcion = models.TextField('Descripción', blank=True)
    costo = models.IntegerField(
        'Costo',
        default=0,
        validators=[MinValueValidator(0)]
    )
    duracion_estimada = models.IntegerField(
        'Duración Estimada (en minutos)', default=0)

    class Meta:
        db_table = 'servicios'
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre_servicio


# Modelo de pago
class Pago(models.Model):
    """Modelo que representa el pago de una cotización."""

    cotizacion = models.ForeignKey(
        Cotizacion,
        related_name='pagos',
        on_delete=models.CASCADE,
        verbose_name='Cotización'
    )
    monto_pagado = models.IntegerField(
        'Monto Pagado',
        default=0,
        validators=[MinValueValidator(0)]
    )
    metodo_pago = models.CharField(
        'Método de Pago',
        max_length=20,
        choices=Cotizacion.MetodoPago.choices,
        default=Cotizacion.MetodoPago.EFECTIVO
    )
    fecha_pago = models.DateTimeField('Fecha de Pago', auto_now_add=True)

    class Meta:
        db_table = 'pagos'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f'Pago {self.monto_pagado} - Cotización {self.cotizacion.numero_cotizacion}'
