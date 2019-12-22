from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Escenario, Trama, Texto, Evento, Etapa, Tipo_Pregunta, Pregunta, Alternativa, Personaje, Rol


@admin.register(User)
class UsuarioAdmin(UserAdmin):
        
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined', 'created_at')}),
    )
    readonly_fields = ['created_at', 'last_login', 'date_joined']


class EscenarioAdmin(admin.ModelAdmin):
    model = Escenario
    list_display = ('nombre', 'created_at', 'activa')

class TramaAdmin(admin.ModelAdmin):
    model = Trama
    list_display = ('nombre', 'escenario', 'fecha_inicio', 'fecha_termino')

class TextoAdmin(admin.ModelAdmin):
    model = Texto
    list_display = ('nombre', 'get_escenario', 'trama')

    def get_escenario(self, obj):
        return obj.trama.escenario
    get_escenario.short_description = 'Escenario'

class EventoAdmin(admin.ModelAdmin):
    model = Evento
    list_display = ('nombre', 'get_escenario', 'get_trama', 'etapa', 'fecha')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        EVENTO = 2
        if db_field.name == "pregunta":
            kwargs["queryset"] = Pregunta.objects.filter(tipo_pregunta = EVENTO)
        return super(EventoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_escenario(self, obj):
        return obj.etapa.trama.escenario

    def get_trama(self, obj):
        return obj.etapa.trama

    get_escenario.short_description = 'Escenario'
    get_trama.short_description = 'Trama'

class EtapaAdmin(admin.ModelAdmin):
    model = Etapa
    list_display = ('nombre', 'get_escenario', 'trama', 'activa', 'etapa_siguiente', 'fecha_inicio', 'fecha_termino')
    ordering = ('fecha_inicio',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        PERFIL = 1
        if db_field.name == "pregunta":
           kwargs["queryset"] = Pregunta.objects.filter(tipo_pregunta = PERFIL)
        return super(EtapaAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        
    def get_escenario(self, obj):
        return obj.trama.escenario
    get_escenario.short_description = 'Escenario'

class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    list_display = ('descripcion', 'tipo_pregunta')
    ordering = ['orden',]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if request.resolver_match.kwargs:
            pregunta_id = int(request.resolver_match.kwargs['object_id'])
            if db_field.name == "alternativas":
                kwargs["queryset"] = Alternativa.objects.filter(pregunta = pregunta_id)
            return super(PreguntaAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class AlternativaAdmin(admin.ModelAdmin):
    model = Alternativa
    list_display = ('descripcion', 'pregunta')

admin.site.register(Escenario, EscenarioAdmin)
admin.site.register(Trama, TramaAdmin)
admin.site.register(Texto, TextoAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Etapa, EtapaAdmin)
admin.site.register(Tipo_Pregunta)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Alternativa, AlternativaAdmin)
admin.site.register(Personaje)
admin.site.register(Rol)
