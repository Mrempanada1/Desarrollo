from .models import Cotizacion, DetalleCotizacion
from django.contrib import admin
from .models import Cotizacion, DetalleCotizacion, Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cotizacion', 'monto', 'estado_pago', 'fecha_pago')
    list_filter = ('estado_pago', 'fecha_pago')
    search_fields = ('cotizacion__id', 'monto')


# Configuración para mostrar Cotizacion en el panel de administración


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehiculo', 'estado', 'total_estimado', 'monto_total',
                    'fecha_creacion')  # Campos que se mostrarán en la lista
    list_filter = ('estado', 'fecha_creacion')  # Filtros laterales
    # Campos por los que se puede buscar
    search_fields = ('vehiculo__patente', 'vehiculo__marca',
                     'vehiculo__modelo', 'estado')
    ordering = ('-fecha_creacion',)  # Orden de las cotizaciones
    # Campos que no se pueden editar
    readonly_fields = ('total_estimado', 'fecha_creacion')
    fieldsets = (
        ('Información General', {
            'fields': ('vehiculo', 'descripcion', 'estado')
        }),
        ('Costos', {
            'fields': ('total_estimado', 'monto_total')
        }),
    )

# Configuración para mostrar DetalleCotizacion en el panel de administración


@admin.register(DetalleCotizacion)
class DetalleCotizacionAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista
    list_display = ('id', 'cotizacion', 'servicio', 'costo_servicio')
    list_filter = ('cotizacion',)  # Filtros laterales
    # Campos por los que se puede buscar
    search_fields = ('cotizacion__id', 'servicio__nombre')
    ordering = ('cotizacion',)  # Orden de los detalles de cotización
