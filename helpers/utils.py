from core.serializers import UserSerializer

def my_jwt_response_handler(token, user=None, request=None):
    print("pase carajo")
    return {
        'success': 'true',
        'data': {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }
    }
    