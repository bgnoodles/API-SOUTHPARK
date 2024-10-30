from django.db import models

# Create your models here.
class Personaje(models.Model):
    nombre = models.CharField(max_length=100,blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    imagen_url = models.URLField(blank=True, null=True)
    primera_aparicion = models.CharField(max_length=100, blank=True, null=True)
    ocupacion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
