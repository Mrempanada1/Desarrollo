from django.contrib import admin
from .models import Dueño, Vehiculo, Servicio, Trabajador, Proceso, Pago, Cita, Cotizacion

admin.site.register(Dueño)
admin.site.register(Vehiculo)
admin.site.register(Servicio)
admin.site.register(Trabajador)
admin.site.register(Proceso)
admin.site.register(Pago)
admin.site.register(Cita)


class VehiculoInline(admin.TabularInline):
    model = Vehiculo
    extra = 1


class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'estado', 'total_estimado', 'fecha_creacion')
    search_fields = ('vehiculo__patente',)
    list_filter = ('estado',)
    readonly_fields = ('total_estimado', 'fecha_creacion')
    ordering = ('-fecha_creacion',)


admin.site.register(Cotizacion, CotizacionAdmin)
