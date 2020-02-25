from system.core.models import (
    User, Story_Category, Story,
    Question, Movement, Answer, Text)
from system.core.serializers import (
    UserSerializer, RegistrationSerializer, UserMeSerializer,
    StoryCategorySerializer, StorySerializer, QuestionSerializer,
    MovementSerializer, AnswerSerializer, TextsSerializer)
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


class StoryCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Story_Category.objects.all()
    serializer_class = StoryCategorySerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)


class StoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)


class QuestionViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)


class TextsViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Text.objects.all()
    serializer_class = TextsSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)


class MovementViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Movement.objects.all()
    serializer_class = MovementSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)

    def create(self, request):
        data = request.data
        try:
            movement = Movement.objects.create(
                usuario_id=data['usuario']
            )
            for respuesta in data['respuestas']:
                Answer.objects.create(
                    pregunta_id=respuesta['pregunta_id'],
                    alternativa_id=respuesta['alternativa_id'],
                    movimiento=movement,
                )
            return created_http_201('SUCCESS')
        except Exception as e:
            raise APIException()


class AnswerViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)