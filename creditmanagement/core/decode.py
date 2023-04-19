# from usercredit.models import User
import jwt
from creditmanagement.settings import SECRET_KEY
# from django.core.exceptions import ValidationError

JWT_ALGORITHM = "HS256"

def get_object(request):
    req =  request.META.get('HTTP_AUTHORIZATION', None)
    if req != '' and req is not None:
        token = req.split(" ", 1)[1]
        if not token:
            return False
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return False
        return payload
    else:
        return False


