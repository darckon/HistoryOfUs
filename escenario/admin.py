from django.contrib import admin
from .models import Escenario, Trama, Texto, Evento, Etapa, Tipo_Pregunta, Pregunta, Opciones_Pegunta

# Register your models here.

admin.site.register(Escenario)
admin.site.register(Trama)
admin.site.register(Texto)
admin.site.register(Evento)
admin.site.register(Etapa)
admin.site.register(Tipo_Pregunta)
admin.site.register(Pregunta)
admin.site.register(Opciones_Pegunta)