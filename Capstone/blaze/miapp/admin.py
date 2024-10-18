from django.contrib import admin
from .models import Dueño, Vehiculo, Servicio, Trabajador, Proceso, Pago, Cita, Cotizacion

admin.site.register(Dueño)
admin.site.register(Vehiculo)
admin.site.register(Servicio)
admin.site.register(Trabajador)
admin.site.register(Proceso)
admin.site.register(Pago)
admin.site.register(Cita)

# Registrando Cotizacion con opciones adicionales


class CotizacionAdmin(admin.ModelAdmin):
    # Ajusta los campos segun lo que quieras mostrar
    list_display = ('vehiculo', 'estado', 'total_estimado', 'fecha_creacion')
    # Permite buscar por patente de vehiculo y nombre del servicio
    search_fields = ('vehiculo__patente',)
    # Permite filtrar por estado
    list_filter = ('estado',)


admin.site.register(Cotizacion, CotizacionAdmin)
