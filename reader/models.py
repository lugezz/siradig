from django.db import models


class RegAccesos(models.Model):
    fecha = models.DateField(auto_now_add=True)
    carpeta = models.CharField(max_length=100, unique=True)
    autenticado = models.BooleanField()


class Registros(models.Model):
    id_reg = models.IntegerField()
    cuil = models.BigIntegerField()
    tipo = models.CharField(max_length=50)
    tipo2 = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.CharField(max_length=50)
    importe = models.CharField(max_length=50)
    par2 = models.CharField(max_length=50, blank=True, null=True)
