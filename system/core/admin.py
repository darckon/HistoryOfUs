from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Story_Category, Story, 
    Text, Event, Step, QuestionType, 
    Question, Alternative, Character, Rol,
    Chapter)


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


@admin.register(Story_Category)
class StoryCategoryAdmin(admin.ModelAdmin):
    model = Story_Category
    list_display = ('name', 'created_at', 'active')


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    model = Story
    list_display = ('name', 'category', 'start_date', 'end_date')


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    model = Text
    list_display = ('name', 'get_story_category', 'chapter')

    def get_story_category(self, obj):
        return obj.chapter.story.category
    get_story_category.short_description = 'Categoria historia'


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    model = Chapter
    list_display = ('name', 'story', 'created_at')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('name', 'get_story_category', 'get_story', 'step', 'date')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        EVENT = 2
        if db_field.name == "question":
            kwargs["queryset"] = Question.objects.filter(question_type = EVENT)
        return super(EventAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_story_category(self, obj):
        return obj.step.story.category

    def get_story(self, obj):
        return obj.step.story

    get_story_category.short_description = 'Categoria historia'
    get_story.short_description = 'Historia'


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    model = Step
    list_display = ('name', 'get_story_category', 'story', 'active', 'next_step', 'start_date', 'end_date')
    ordering = ('start_date',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        PERFIL = 1
        if db_field.name == "pregunta":
           kwargs["queryset"] = Question.objects.filter(question_type = PERFIL)
        return super(StepAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
        
    def get_story_category(self, obj):
        return obj.story.category
    get_story_category.short_description = 'Categoria historia'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ('name', 'question_type')
    ordering = ['order',]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if request.resolver_match.kwargs:
            pregunta_id = int(request.resolver_match.kwargs['object_id'])
            if db_field.name == "alternatives":
                kwargs["queryset"] = Alternative.objects.filter(question = pregunta_id)
            return super(QuestionAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Alternative)
class AlternativeAdmin(admin.ModelAdmin):
    model = Alternative
    list_display = ('description', 'get_question')
    list_filter = ('question__question_type__name',)
    search_fields = ('description',)
    list_per_page = 20

    def get_question(self, obj):
        return obj.question.name
    get_question.short_description = 'Pregunta'


admin.site.register(QuestionType)
admin.site.register(Character)
admin.site.register(Rol)
