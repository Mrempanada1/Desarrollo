from django.contrib import admin
from .models import Dueño, Vehiculo, Reparacion, Servicio, Trabajador, Proceso, Pago, Cita, Cotizacion

admin.site.register(Dueño)
admin.site.register(Vehiculo)
admin.site.register(Reparacion)
admin.site.register(Servicio)
admin.site.register(Trabajador)
admin.site.register(Proceso)
admin.site.register(Pago)
admin.site.register(Cita)
admin.site.register(Cotizacion)


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    # Ajusta los campos segun lo que quieras mostrar
    list_display = ('vehiculo', 'servicio', 'monto_estimado', 'estado')
    # Permite busqueda por patente de vehículo y nombre del servicio
    search_fields = ('vehiculo__patente', 'servicio__nombre_servicio')
