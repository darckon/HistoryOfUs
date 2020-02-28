from system.core.models import (
    User, Story_Category, Story, Question,
    Movement, Answer, Text, Character)
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
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction as atomic_transaction
from config.constants import MOVEMENT_TYPE



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
            with atomic_transaction.atomic():

                movement = Movement.objects.create(
                    user_id=data['user'],
                    movement_type = data['movement_type']
                )
                
                if movement.movement_type == MOVEMENT_TYPE['INITIAL_CHARACTER_CONFIGURATION']:
                    for value in data['answers']:
                        found_duplicate_question = Answer.objects.filter(
                            question_id= value['question_id'],
                            movement__user= data['user']).first()
                        if found_duplicate_question:
                            raise APIException('duplicado')
                    
                        Character.objects.create(
                            name = vale['']
                        )   

                        Answer.objects.create(
                            question_id=value['question_id'],
                            alternative_id=value['alternative_id'],
                            movement=movement,
                        )

                return created_http_201('SUCCESS')
        except Exception as e:
            print('pase')
            print(e)
            atomic_transaction.rollback()
            print('yep')
            raise APIException(e)


class AnswerViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_fields = '__all__'
    filter_backends = (UrlDjangoFilterBackend,)