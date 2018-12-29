from django.db import models

# Create your models here.

class Escenario(models.Model):
    nombre = models.CharField('Escenario', max_length = 100)
    activa = models.BooleanField(default = True)
    def __str__(self):
        return self.nombre

class Trama(models.Model):
    nombre    = models.CharField('Trama' , max_length = 250)
    escenario = models.ForeignKey(Escenario, on_delete=models.PROTECT)
    inicio    = models.DateField('Fecha Inicio', null = True)
    fin       = models.DateField('Fecha Termino', null = True)
    def __str__(self):
        return "%s | %s " % (self.nombre, self.escenario)

class Texto(models.Model):
    nombre   = models.CharField('Nombre', max_length = 100)
    texto    = models.TextField('Descripcion')
    contexto = models.ForeignKey(Trama, on_delete=models.PROTECT)
    def __str__(self):
        return "%s | %s " % (self.nombre, self.contexto)

class Evento(models.Model):
    nombre = models.CharField('Nombre' , max_length = 100)
    fecha  = models.DateTimeField('Fecha Evento', null=True, blank=True)
    trama  = models.ForeignKey(Trama, on_delete=models.PROTECT)
    def __str__(self):
        return "%s | %s " % (self.nombre, self.trama)
