# -*- encoding: utf-8 -*-
from system.core.models import (
    User, Personaje, Categoria_Historia,
    Historia, Pregunta, Alternativa)
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework_jwt.settings import api_settings


class MyCustomExcpetion(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Custom Exception Message"
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

class PersonajeSerializer(serializers.ModelSerializer):
    escenario_id = serializers.ReadOnlyField(source='trama.escenario.id')
    escenario_nombre = serializers.ReadOnlyField(source='trama.escenario.nombre')
    trama_id = serializers.ReadOnlyField(source='trama.id')
    trama_nombre = serializers.ReadOnlyField(source='trama.nombre')
    rol_id = serializers.ReadOnlyField(source='rol.id')
    rol_nombre = serializers.ReadOnlyField(source='rol.nombre')
    class Meta:
        model = Personaje
        fields = ('id', 'escenario_id', 'escenario_nombre', 'trama_id', 'trama_nombre', 'rol_id', 'rol_nombre')

class UserMeSerializer(serializers.ModelSerializer):
    personaje = PersonajeSerializer(source='personaje_set', many=True)
    class Meta:
        model = User
        fields = ('id','username','email', 'personaje')

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def to_representation(self, instance):
        # instance is the model object. create the custom json format by accessing instance attributes normaly and return it
        identifiers = dict()
        identifiers['email'] = instance.email
        identifiers['username'] = instance.username
        representation = {
            'success': 'true',
            'data': identifiers,
        }
        return representation

    def create(self, validated_data):
        print('pase')
        user = super(RegistrationSerializer, self).create(validated_data)
        user.set_password(self.context['request'].data['password'])
        user.email = self.context['request'].data['email']
        user.save()
        return user


class CategoriaHistoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria_Historia
        fields = ('id','nombre', 'activa')


class HistoriaSerializer(serializers.ModelSerializer):
    categoria_set = CategoriaHistoriaSerializer(source='categoria', read_only=True)
    class Meta:
        model = Historia
        fields = (
            'id','nombre', 'categoria_set', 
            'fecha_inicio', 'fecha_termino', 'activa')



class AlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alternativa
        fields = (
            'id','descripcion',)


class PreguntaSerializer(serializers.ModelSerializer):
    alternativas_set = AlternativaSerializer(source='alternativas', many=True, read_only=True)
    class Meta:
        model = Pregunta
        fields = (
            'descripcion','tipo_pregunta', 'rol', 
            'alternativas_set', 'orden')