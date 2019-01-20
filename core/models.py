from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    #escenario = models.ManyToManyField('core.Escenario', related_name='escenarios')
    personaje = models.ManyToManyField('core.Trama', related_name='personajes', through='core.Personaje')
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)
        
    class Meta:
        """ 
        User.
            username
            password
            first_name
            last_name
            email
            is_staff
            is_active
            date_joined
        """
        ordering = ('first_name', )
        verbose_name = ("Usuario")
        verbose_name_plural = ("Usuarios")

class Personaje(models.Model):
    user = models.ForeignKey("core.User", db_index=True, related_name='users', verbose_name=("usuario"), on_delete=models.CASCADE, unique=True)
    trama = models.ForeignKey("core.Trama", db_index=True, related_name='personaje_trama', verbose_name=("trama"), on_delete=models.CASCADE)
    rol = models.ForeignKey('core.Rol', verbose_name=("Rol"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Personaje")
        verbose_name_plural = ("Personajes")

    def __str__(self):
        return '%s :: %s' % (self.user, self.trama)

class Rol(models.Model):
    nombre = models.CharField('nombre', max_length = 100)
    stock = models.IntegerField('Stock', help_text='Cantidad total disponible de roles en la historia')
    stock_ocupado = models.IntegerField('Stock ocupado', help_text='Total de roles ocupados hasta el momento')
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Rol")
        verbose_name_plural = ("Roles")

    def __str__(self):
        return self.nombre

class Escenario(models.Model):
    nombre = models.CharField('Escenario', max_length = 100)
    activa = models.BooleanField(default = True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Escenario")
        verbose_name_plural = ("Escenarios")

    def __str__(self):
        return self.nombre

class Trama(models.Model):
    nombre = models.CharField('Trama' , max_length = 250)
    escenario = models.ForeignKey(Escenario, on_delete=models.PROTECT)
    fecha_inicio = models.DateField('Fecha Inicio', null = True)
    fecha_termino = models.DateField('Fecha Termino', null = True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Trama")
        verbose_name_plural = ("Tramas")

    def __str__(self):
        return self.nombre

class Texto(models.Model):
    nombre = models.CharField('Nombre', max_length = 100)
    texto = models.TextField('Texto')
    trama = models.ForeignKey(Trama, on_delete=models.PROTECT)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)
    
    class Meta:
        verbose_name = ("Texto")
        verbose_name_plural = ("Textos")
    
    def __str__(self):
        return self.nombre

class Etapa(models.Model):
    nombre = models.CharField('Nombre' , max_length = 100)
    trama = models.ForeignKey(Trama, on_delete=models.PROTECT)
    pregunta = models.ManyToManyField("core.Pregunta", related_name='etapa_preguntas', verbose_name='Pregunta(Perfil)')
    etapa_siguiente = models.ForeignKey("core.Etapa", related_name='siguiente', on_delete=models.PROTECT, null = True, blank=True)
    activa = models.BooleanField(default=False)
    fecha_inicio = models.DateField('Fecha Inicio', null = True)
    fecha_termino = models.DateField('Fecha Termino', null = True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)
    
    class Meta:
        verbose_name = ("Etapa")
        verbose_name_plural = ("Etapas")

    def __str__(self):
        return '%s | %s' % (self.nombre , self.trama)

class Evento(models.Model):
    nombre = models.CharField('Nombre' , max_length = 100)
    etapa = models.ForeignKey(Etapa, on_delete=models.PROTECT)
    fecha = models.DateTimeField('Fecha Evento', null=True, blank=True)
    pregunta = models.ManyToManyField('core.Pregunta', related_name='evento_preguntas')
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Evento")
        verbose_name_plural = ("Eventos")

    def __str__(self):
        return self.nombre

class Tipo_Pregunta(models.Model):
    nombre = models.CharField('Nombre' , max_length = 100)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Tipo Pregunta")
        verbose_name_plural = ("Tipos Preguntas")
    
    def __str__(self):
        return self.nombre


class Pregunta(models.Model):
    descripcion = models.TextField('Descripcion')
    tipo_pregunta = models.ForeignKey(Tipo_Pregunta, on_delete=models.PROTECT)
    rol = models.ManyToManyField(Rol, related_name='roles')
    alternativas = models.ManyToManyField("core.Alternativa", related_name='alternativas')
    orden = models.IntegerField("Orden", null=True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Pregunta")
        verbose_name_plural = ("Preguntas")

    def __str__(self):
        return self.descripcion

class Alternativa(models.Model):
    descripcion = models.TextField('Descripcion')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Alternativa")
        verbose_name_plural = ("Alternativas")

    def __str__(self):
        return self.descripcion


