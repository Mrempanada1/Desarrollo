from django.urls import path
from . import views

urlpatterns = [
    path('crear_cotizacion/', views.crear_cotizacion, name='crear_cotizacion'),
    path('pagar_cotizacion/<uuid:cotizacion_id>/',
         views.pagar_cotizacion, name='pagar_cotizacion'),
    path('pago_exitoso/<uuid:cotizacion_id>/',
         views.pago_exitoso, name='pago_exitoso'),
    path('pago_fallido/<uuid:cotizacion_id>/',
         views.pago_fallido, name='pago_fallido'),
    path('pago_pendiente/<uuid:cotizacion_id>/',
         views.pago_pendiente, name='pago_pendiente'),
    path('notificaciones_pago/', views.notificaciones_pago,
         name='notificaciones_pago'),
]
