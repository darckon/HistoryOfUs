from system.core.models import (
    User, Categoria_Historia, Historia)
from system.core.serializers import (
    UserSerializer, RegistrationSerializer, UserMeSerializer,
    CategoriaHistoriaSerializer, HistoriaSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from url_filter.integrations.drf import DjangoFilterBackend as UrlDjangoFilterBackend
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


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
    
    @list_route(methods=['get'], url_path='me')
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