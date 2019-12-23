from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Categoria_Historia, Historia, Texto, Evento, Etapa, Tipo_Pregunta, Pregunta, Alternativa, Personaje, Rol


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


class CategoriaHistoriaAdmin(admin.ModelAdmin):
    model = Categoria_Historia
    list_display = ('nombre', 'created_at', 'activa')

class HistoriaAdmin(admin.ModelAdmin):
    model = Historia
    list_display = ('nombre', 'categoria', 'fecha_inicio', 'fecha_termino')

class TextoAdmin(admin.ModelAdmin):
    model = Texto
    list_display = ('nombre', 'get_categoria_historia', 'historia')

    def get_categoria_historia(self, obj):
        return obj.historia.categoria_historia
    get_categoria_historia.short_description = 'Categoria historia'

class EventoAdmin(admin.ModelAdmin):
    model = Evento
    list_display = ('nombre', 'get_categoria_historia', 'get_historia', 'etapa', 'fecha')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        EVENTO = 2
        if db_field.name == "pregunta":
            kwargs["queryset"] = Pregunta.objects.filter(tipo_pregunta = EVENTO)
        return super(EventoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_categoria_historia(self, obj):
        return obj.etapa.historia.categoria_historia

    def get_historia(self, obj):
        return obj.etapa.historia

    get_categoria_historia.short_description = 'Categoria historia'
    get_historia.short_description = 'Historia'

class EtapaAdmin(admin.ModelAdmin):
    model = Etapa
    list_display = ('nombre', 'get_categoria_historia', 'historia', 'activa', 'etapa_siguiente', 'fecha_inicio', 'fecha_termino')
    ordering = ('fecha_inicio',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        PERFIL = 1
        if db_field.name == "pregunta":
           kwargs["queryset"] = Pregunta.objects.filter(tipo_pregunta = PERFIL)
        return super(EtapaAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        
    def get_categoria_historia(self, obj):
        return obj.historia.categoria_historia
    get_categoria_historia.short_description = 'Categoria historia'

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

admin.site.register(Categoria_Historia, CategoriaHistoriaAdmin)
admin.site.register(Historia, HistoriaAdmin)
admin.site.register(Texto, TextoAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Etapa, EtapaAdmin)
admin.site.register(Tipo_Pregunta)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Alternativa, AlternativaAdmin)
admin.site.register(Personaje)
admin.site.register(Rol)
