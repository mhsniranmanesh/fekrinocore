from channels.auth import AuthMiddlewareStack
from django.contrib.auth import get_user_model
from jwt import exceptions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_jwt.authentication import jwt_get_username_from_payload


class JWTAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def authenticate_credentials(self, payload):
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        if b'Authorization' in headers:
            try:
                print('Auth')
                token_name, token_key = headers[b'Authorization'].decode().split()
                if token_name == 'JWT':
                    user = self.authenticate_credentials(token_key)
                    scope['user'] = user
                    close_old_connections()
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        return self.inner(scope)

JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))

