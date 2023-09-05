from usercredit.models import User
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
import jwt
from creditmanagement.settings import SECRET_KEY

from core.decode import get_object

JWT_ALGORITHM = "HS256"

@database_sync_to_async
def get_user(token):
    if token:
        payload = jwt.decode(token , SECRET_KEY , algorithms=JWT_ALGORITHM)
        if payload:
            user = User.objects.get(id = payload["user_id"], is_admin= True)
        else:
            user = AnonymousUser()
    else:
        user = AnonymousUser()
    return user
 
class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app
 
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        token = query_dict["token"][0]
        user = await get_user(token)
        scope["user"] = user
        return await self.app(scope, receive, send)