import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import mercadopago
from .models import Cotizacion, Pago
from django.contrib import messages

# Configurar MercadoPago
mp = mercadopago.MP(settings.MP_ACCESS_TOKEN)

# Vista para ver detalles de la cotización y el botón de pago


def cotizacion_detalle(request, cotizacion_id):
    cotizacion = Cotizacion.objects.get(id=cotizacion_id)

    # Crear un objeto de preferencia para MercadoPago
    preference_data = {
        "items": [
            {
                "title": f"Cotización {cotizacion.numero_cotizacion}",
                "quantity": 1,
                # Convertimos a cantidad en unidades monetarias
                "unit_price": cotizacion.total / 100,
                "currency_id": "ARS",
            }
        ],
        "payer": {
            "name": cotizacion.dueño.get_full_name() if cotizacion.dueño else 'Anónimo',
            "email": cotizacion.dueño.email if cotizacion.dueño else 'example@example.com',
        },
        "back_urls": {
            "success": request.build_absolute_uri(f"/cotizacion/{cotizacion.id}/exitoso/"),
            "failure": request.build_absolute_uri(f"/cotizacion/{cotizacion.id}/fallido/"),
            "pending": request.build_absolute_uri(f"/cotizacion/{cotizacion.id}/pendiente/"),
        },
        "auto_return": "approved",
        "notification_url": request.build_absolute_uri("/notificacion_pago/")
    }

    # Crear preferencia
    preference = mp.preferences.create(preference_data)

    if preference["status"] == "created":
        cotizacion.numero_cotizacion = preference["response"]["id"]
        cotizacion.save()

    return render(request, "cotizaciones/cotizacion_detalle.html", {
        'cotizacion': cotizacion,
        'preference_id': preference["response"]["id"],
        'preference_url': preference["response"]["init_point"]
    })


# Vista para manejar la respuesta de MercadoPago al éxito del pago
@csrf_exempt
def pago_exitoso(request, cotizacion_id):
    cotizacion = Cotizacion.objects.get(id=cotizacion_id)
    payment_id = request.GET.get('payment_id')
    status = request.GET.get('status')

    if status == "approved":
        # Registrar el pago en el sistema
        Pago.objects.create(
            cotizacion=cotizacion,
            monto_pagado=cotizacion.total,
            metodo_pago=cotizacion.metodo_pago,
            fecha_pago=cotizacion.fecha_cotizacion,
        )
        cotizacion.estado = "aprobada"
        cotizacion.save()

        messages.success(request, "¡Pago aprobado con éxito!")
        return redirect("cotizacion_detalle", cotizacion_id=cotizacion.id)
    else:
        messages.error(request, "El pago no fue aprobado.")
        return redirect("cotizacion_detalle", cotizacion_id=cotizacion.id)


# Vista para manejar la respuesta de MercadoPago al fallo del pago
@csrf_exempt
def pago_fallido(request, cotizacion_id):
    cotizacion = Cotizacion.objects.get(id=cotizacion_id)
    messages.error(request, "El pago ha fallado.")
    return redirect("cotizacion_detalle", cotizacion_id=cotizacion.id)


# Vista para manejar la respuesta de MercadoPago en caso de un pago pendiente
@csrf_exempt
def pago_pendiente(request, cotizacion_id):
    cotizacion = Cotizacion.objects.get(id=cotizacion_id)
    messages.warning(
        request, "El pago está pendiente. Por favor, verifica el estado del pago.")
    return redirect("cotizacion_detalle", cotizacion_id=cotizacion.id)


# Vista para notificación de pago a través de la URL configurada
@csrf_exempt
def notificacion_pago(request):
    data = json.loads(request.body)
    payment_id = data["data"]["id"]

    # Obtenemos el pago
    payment_info = mp.payment.find_by_id(payment_id)
    payment_status = payment_info["response"]["status"]

    if payment_status == "approved":
        # Actualizamos el estado de la cotización y guardamos el pago
        cotizacion = Cotizacion.objects.get(
            numero_cotizacion=payment_info["response"]["order"]["id"])
        cotizacion.estado = "aprobada"
        cotizacion.save()

        Pago.objects.create(
            cotizacion=cotizacion,
            monto_pagado=cotizacion.total,
            metodo_pago=cotizacion.metodo_pago,
            fecha_pago=cotizacion.fecha_cotizacion,
        )

    return JsonResponse({"status": "success"})


# Vista para crear una cotización desde el panel de administración
def crear_cotizacion(request):
    if request.method == 'POST':
        # Crear una nueva cotización
        cotizacion = Cotizacion.objects.create(
            dueño=request.user,
            subtotal=1000,  # Ejemplo, deberías calcularlo con base en los servicios
            impuestos=190,  # Ejemplo
            total=1190,  # Ejemplo
            metodo_pago="efectivo",
            estado="pendiente",
            supervisor=request.user
        )
        cotizacion.save()
        return redirect("cotizacion_detalle", cotizacion_id=cotizacion.id)

    return render(request, "cotizaciones/crear_cotizacion.html")
