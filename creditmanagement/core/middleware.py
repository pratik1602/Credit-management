from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from creditmanagement.settings import SIMPLE_JWT, SECRET_KEY
import jwt
from usercredit.models import *

@database_sync_to_async
def get_user(token_key):
    try:
        user_id: int = jwt.decode(token_key, SECRET_KEY, algorithms=[SIMPLE_JWT['ALGORITHM']]).get(SIMPLE_JWT['USER_ID_CLAIM'])
    except jwt.exceptions.DecodeError:
        return AnonymousUser()
    except jwt.exceptions.ExpiredSignatureError:
        return AnonymousUser()
    try:
        return AnonymousUser() if user_id is None else User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)












# from channels.middleware import BaseMiddleware
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
# from rest_framework_simplejwt.tokens import UntypedToken


# User = get_user_model()

# class JWTAuthMiddleware(BaseMiddleware):
    
#     def __init__(self, inner):
#         super().__init__(inner)

#     async def __call__(self, scope, receive, send):
#         headers = dict(scope["headers"])
#         if b"authorization" in  headers:
#             try:
#                 token_name, token_key = headers[b"authorization"].decode().split()
#                 if token_name.lower() == "bearer":
#                     validated_token = UntypedToken(token_key)
#                     user_id = validated_token["user_id"]
#                     try:
#                         scope["user"] = await self.get_user(user_id)
#                     except User.DoesNotExist:
#                         pass
#             except (InvalidToken, TokenError):
#                 pass
#         return await super().__call__(scope, receive, send)
    
#     @staticmethod
#     async def get_user(user_id):
#         try:
#             return await User.objects.get(id = user_id)
#         except User.DoesNotExist:
#             pass

# def JwtAuthMiddlewareStack(inner):
#     return JWTAuthMiddleware(inner)