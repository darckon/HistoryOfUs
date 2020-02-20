from rest_framework import status
from rest_framework.response import Response
from system.core.helpers.constants import RESPONSE_STATUS 


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token
    }

def created_http_201(message):
    return Response(RESPONSE_STATUS[message], status=status.HTTP_201_CREATED)
    