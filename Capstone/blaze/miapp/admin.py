from django.contrib import admin
from .models import Dueño, Vehiculo, Reparacion, Servicio, Trabajador, Proceso, Pago, Cita

admin.site.register(Dueño)
admin.site.register(Vehiculo)
admin.site.register(Reparacion)
admin.site.register(Servicio)
admin.site.register(Trabajador)
admin.site.register(Proceso)
admin.site.register(Pago)
admin.site.register(Cita)
