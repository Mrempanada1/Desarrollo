# from fcm_django.api.rest import FCMError
# from fcm_django.fcm import FCMDevice


# def enviar_notificacion(mensaje, dispositivo_token):
# try:
# device = FCMDevice.objects.get(registration_id=dispositivo_token)
# device.send_message(title="Notificación", body=mensaje)
# except FCMError as e:
# print(f"Error enviando notificación: {e}")
