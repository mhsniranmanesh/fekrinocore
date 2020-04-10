from asgiref.sync import sync_to_async
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenVerifySerializer

from profiles.models.user import User


class JWTAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        jwt_auth = JWTAuthentication()
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name == 'JWT':
                data = {'token': token_key}
                valid_data  = TokenVerifySerializer().validate(data)
                print(valid_data)
                validated_token = jwt_auth.get_validated_token(token_key)
                # user = sync_to_async(jwt_auth.get_user)(validated_token).run()
                print("HEHEHE")
                user = User.objects.get(id=1)
                scope['user'] = user

            scope['user'] = AnonymousUser()
        return self.inner(scope)

JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))