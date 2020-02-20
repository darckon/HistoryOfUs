from system.core.models import (
    User, Categoria_Historia, Historia,
    Pregunta, Movimientos, Respuestas)
from system.core.serializers import (
    UserSerializer, RegistrationSerializer, UserMeSerializer,
    CategoriaHistoriaSerializer, HistoriaSerializer, PreguntaSerializer,
    MovimientosSerializer, RespuestasSerializer)
from system.core.helpers.utils import created_http_201
from django_filters.rest_framework import DjangoFilterBackend
from url_filter.integrations.drf import DjangoFilterBackend as UrlDjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.exceptions import APIException
from rest_framework import status, viewsets


class RegistrationViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    filter_fields = '__all__'


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = '__all__'
    filter_backends = (DjangoFilterBackend,)
    
    @action(detail=False, methods=['get'], url_path='me')
    def getUser(self, request):
        user = User.objects.get(pk = request.user.pk)
        serializer = UserMeSerializer(user)
        if serializer.data:
            response = Response({'success':'true', 'data': serializer.data})
        return response


class CategoriaHistoriaViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Categoria_Historia.objects.all()
    serializer_class = CategoriaHistoriaSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)


class HistoriaViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Historia.objects.all()
    serializer_class = HistoriaSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)


class PreguntasViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)


class MovimientosViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Movimientos.objects.all()
    serializer_class = MovimientosSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)

    def create(self, request):
        data = request.data
        try:
            movimiento = Movimientos.objects.create(
                usuario_id=data['usuario']
            )
            for respuesta in data['respuestas']:
                Respuestas.objects.create(
                    pregunta_id=respuesta['pregunta_id'],
                    alternativa_id=respuesta['alternativa_id'],
                    movimiento=movimiento,
                )
            return created_http_201('SUCCESS')
        except Exception as e:
            raise APIException()


class RespuestasViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Respuestas.objects.all()
    serializer_class = RespuestasSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)