from django.db import models
from django.contrib.auth.models import User


class Vehiculo(models.Model):
    # Campos para el registro del vehículo
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    año = models.IntegerField()
    color = models.CharField(max_length=50)
    patente = models.CharField(max_length=10, default='SIN PATENTE')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.año} {self.patente}"
