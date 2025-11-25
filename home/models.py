from django.db import models
from django.utils import timezone
# Create your models here.

class Usuarios(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Agregar_categoria(models.Model):
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria
    
class Agregar_Datos(models.Model):
    categoria = models.ForeignKey('Agregar_categoria', on_delete=models.CASCADE, default=1)
    tiempo = models.DateTimeField(default=timezone.now)  # hora de inicio
    duracion = models.DurationField()  # duración tipo timedelta

    def __str__(self):
        return f"{self.categoria} - {self.duracion}"