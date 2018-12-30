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
    trama = models.ForeignKey(Trama, on_delete=models.PROTECT)
    def __str__(self):
        return "%s | %s " % (self.nombre, self.trama)

class Etapa(models.Model):
    nombre = models.CharField('Nombre' , max_length = 100)
    inicio = models.DateField('Fecha Inicio', null = True)
    fin    = models.DateField('Fecha Termino', null = True)
    trama  = models.ForeignKey(Trama, on_delete=models.PROTECT)
    def __str__(self):
        return "%s | %s" % (self.nombre, self.trama)

class Evento(models.Model):
    nombre = models.CharField('Nombre' , max_length = 100)
    fecha  = models.DateTimeField('Fecha Evento', null=True, blank=True)
    etapa  = models.ForeignKey(Etapa, on_delete=models.PROTECT)
    def __str__(self):
        return "%s | %s " % (self.nombre, self.etapa)

class Tipo_Pregunta(models.Model):
    nombre = models.CharField('Nombre' , max_length = 100)
    def __str__(self):
        return "%s" % (self.nombre)

class Opciones_Pegunta(models.Model):
    nombre = models.CharField('Nombre' , max_length = 100)
    trama  = models.ForeignKey(Trama, on_delete=models.PROTECT)
    def __str__(self):
        return "%s | %s" % (self.nombre, self.trama)

class Pregunta(models.Model):
    nombre        = models.CharField('Nombre' , max_length = 100)
    descripcion   = models.TextField('Descripcion')
    opciones      = models.ManyToManyField(Opciones_Pegunta)
    tipo_pregunta = models.ForeignKey(Tipo_Pregunta, on_delete=models.PROTECT)
    evento  = models.ForeignKey(Evento, null = True, blank = True, on_delete=models.PROTECT)
    etapa   = models.ManyToManyField(Etapa,  null = True, blank = True )
    def __str__(self):
        return "%s | %s " % (self.nombre, self.tipo_pregunta)

