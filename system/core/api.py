from system.core.models import User
from system.core.serializers import UserSerializer, RegistrationSerializer, UserMeSerializer
from django_filters.rest_framework import DjangoFilterBackend
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

    