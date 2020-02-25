from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
import uuid

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_index=True, editable=False)
    character = models.ManyToManyField('core.Story', related_name='characters', through='core.Character')
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

class Character(models.Model):
    name = models.CharField('nombre', max_length = 100, unique=True)
    user = models.OneToOneField("core.User", db_index=True, related_name='character_set', verbose_name=("usuario"), on_delete=models.CASCADE)
    story = models.ForeignKey("core.Story", db_index=True, related_name='character_set', verbose_name=("historia"), on_delete=models.CASCADE)
    rol = models.ForeignKey('core.Rol', verbose_name=("Rol"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Personaje")
        verbose_name_plural = ("Personajes")

    def __str__(self):
        return '%s :: %s' % (self.name, self.story)

class Rol(models.Model):
    name = models.CharField('nombre', max_length = 100)
    stock = models.IntegerField('Stock', help_text='Cantidad total disponible de roles en la historia')
    stock_taken = models.IntegerField('Stock ocupado', help_text='Total de roles ocupados hasta el momento')
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Rol")
        verbose_name_plural = ("Roles")

    def __str__(self):
        return self.name

class Story_Category(models.Model):
    name = models.CharField('Nombre', max_length = 100)
    active = models.BooleanField(default = True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Categoria de Historia")
        verbose_name_plural = ("Categoria de Historias")

    def __str__(self):
        return self.name

class Story(models.Model):
    name = models.CharField('Nombre' , max_length = 250)
    category = models.ForeignKey(Story_Category, on_delete=models.PROTECT)
    start_date = models.DateField('Fecha Inicio', null = True)
    end_date = models.DateField('Fecha Termino', null = True)
    active = models.BooleanField(default = True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Historia")
        verbose_name_plural = ("Historias")

    def __str__(self):
        return self.name

class Text(models.Model):
    name = models.CharField('nombre', max_length = 100)
    description = RichTextField('texto', config_name='awesome_ckeditor')
    question = models.ManyToManyField("core.Question", blank=True)
    chapter = models.ForeignKey(
        "core.Chapter", on_delete=models.CASCADE)
    order = models.IntegerField("Orden", null=True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)
    
    class Meta:
        verbose_name = ("Texto")
        verbose_name_plural = ("Textos")
        ordering = ['order']

    
    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField('Nombre', max_length = 100)
    story = models.ForeignKey('core.Story', on_delete=models.CASCADE)
    order = models.IntegerField("Orden", null=True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)
    
    class Meta:
        verbose_name = ("Capitulo")
        verbose_name_plural = ("Capitulos")
        ordering = ['order']
        
    
    def __str__(self):
        return "%s :: %s" % (self.name, self.story)

class Step(models.Model):
    name = models.CharField('Nombre' , max_length = 100)
    story = models.ForeignKey("core.Story", on_delete=models.PROTECT)
    question = models.ManyToManyField("core.Question", related_name='etapa_preguntas', verbose_name='Pregunta(Perfil)')
    next_step = models.ForeignKey("core.Step", related_name='siguiente', on_delete=models.PROTECT, null = True, blank=True)
    active = models.BooleanField(default=False)
    start_date = models.DateField('Fecha Inicio', null = True)
    end_date = models.DateField('Fecha Termino', null = True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)
    
    class Meta:
        verbose_name = ("Etapa")
        verbose_name_plural = ("Etapas")

    def __str__(self):
        return '%s | %s' % (self.name , self.story)

class Event(models.Model):
    name = models.CharField('Nombre' , max_length = 100)
    step = models.ForeignKey(Step, on_delete=models.PROTECT)
    date = models.DateTimeField('Fecha Evento', null=True, blank=True)
    pregunta = models.ManyToManyField('core.Question', related_name='evento_preguntas')
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Evento")
        verbose_name_plural = ("Eventos")

    def __str__(self):
        return self.nombre

class QuestionType(models.Model):
    name = models.CharField('Nombre' , max_length = 100)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        db_table = "core_question_type"
        verbose_name = ("Tipo Pregunta")
        verbose_name_plural = ("Tipos Preguntas")
    
    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField('Titulo', max_length = 100)
    description = RichTextField('Descripcion', config_name='awesome_ckeditor')
    question_type = models.ForeignKey(QuestionType, on_delete=models.PROTECT)
    rol = models.ManyToManyField(Rol, related_name='roles', blank=True)
    alternatives = models.ManyToManyField("core.Alternative", related_name='alternativas')
    order = models.IntegerField("Orden", null=True)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        ordering = ['order']
        verbose_name = ("Pregunta")
        verbose_name_plural = ("Preguntas")

    def __str__(self):
        return self.name

class Alternative(models.Model):
    # Alternatives Choices
    TRANSACTION_CHOICES = [
        (0, 'STRING'),
        (1, 'INPUT')
    ]
    description = RichTextField('Descripcion', config_name='awesome_ckeditor')
    question = models.ForeignKey("core.Question", on_delete=models.PROTECT, blank=True, null=True)
    alternative_type = models.IntegerField(
        'Tipo alternativa', choices=TRANSACTION_CHOICES, default=1)
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Alternativa")
        verbose_name_plural = ("Alternativas")

    def __str__(self):
        return self.description


class TipoAlternativa(models.Model):
    nombre = models.CharField('Nombre', max_length = 100)

    class Meta:
        verbose_name = ("Tipo Alternativa")
        verbose_name_plural = ("Tipos de Alternativas")

    def __str__(self):
        return self.nombre


class Movement(models.Model):
    user = models.ForeignKey("core.User", on_delete=models.PROTECT)
    answer = models.ManyToManyField(
        'core.Question',
        through='core.Answer')
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True) 

    class Meta:
        verbose_name = ("Movimiento")
        verbose_name_plural = ("Movimientos")

    def __str__(self):
        return self.user


class Answer(models.Model):
    question = models.ForeignKey("core.Question", db_index=True,
        on_delete=models.CASCADE,
        related_name='core_question_answer_set')
    alternative = models.ForeignKey(Alternative,db_index=True,
        on_delete=models.CASCADE,
        related_name='core_question_answer_set')
    movement = models.ForeignKey(Movement, db_index=True,
        on_delete=models.CASCADE,
        related_name='core_question_answer_set')
    created_at = models.DateTimeField(("creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(("actualizado el"), auto_now=True)

    class Meta:
        verbose_name = ("Movimiento")
        verbose_name_plural = ("Movimientos")


