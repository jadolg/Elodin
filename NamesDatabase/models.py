from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Name(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return self.nombre + ' -->' + self.ip


class Log(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    usuario = models.CharField(max_length=255)
    ip_usuario = models.CharField(max_length=255)
    accion = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return '['+str(self.fecha)+'] '+self.usuario+' ('+self.accion+') ['+self.nombre + ' -->' + self.ip+"]"