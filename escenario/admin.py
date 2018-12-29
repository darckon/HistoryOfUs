from django.contrib import admin
from .models import Escenario, Trama, Texto, Evento

# Register your models here.

admin.site.register(Escenario)
admin.site.register(Trama)
admin.site.register(Texto)
admin.site.register(Evento)