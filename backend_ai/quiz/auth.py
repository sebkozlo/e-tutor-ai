import jwt
from ninja.security import HttpBearer
from ninja.errors import HttpError
from django.conf import settings


class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            return payload  # You can return user info or any relevant data from the payload
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Invalid token")
