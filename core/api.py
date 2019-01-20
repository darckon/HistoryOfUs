from core.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from core.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = '__all__'
    filter_backends = (DjangoFilterBackend,)