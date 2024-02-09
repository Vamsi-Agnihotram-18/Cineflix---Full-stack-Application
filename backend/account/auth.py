from datetime import datetime, timedelta

from core.errors import ErrorCodes, InvalidAuthentication
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from account.models import CustomUser, CustomToken

class CustomAPIAccessAuthentication(BaseAuthentication):
    JWT_KEYWORD = "bearer"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        lower_keyword = auth[0].lower()
        if lower_keyword != self.JWT_KEYWORD.encode():
            return None

        if len(auth) == 1:
            raise InvalidAuthentication(
                "Invalid token header. No credentials provided.", code=ErrorCodes.access_token_invalid
            )
        elif len(auth) > 2:
            raise InvalidAuthentication(
                "Invalid token header. Token string should not contain spaces.", code=ErrorCodes.access_token_invalid
            )

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise InvalidAuthentication(
                "Invalid token header. Token string should not contain invalid characters.",
                code=ErrorCodes.access_token_invalid,
            )

        return self.authenticate_jwt(token)

    def authenticate_jwt(self, token):
        try:
            app_config = apps.get_app_config("account")
            decoded_token = decode(
                token,
                app_config.BACKEND_JWT_SECRET,
                audience=app_config.BACKEND_JWT_AUD,
                algorithms=["HS256"],
            )
        except ExpiredSignatureError:
            raise InvalidAuthentication("Signature expired.", code=ErrorCodes.access_token_expired)
        except DecodeError:
            raise InvalidAuthentication("Malformed token.", code=ErrorCodes.access_token_malformed)
        except UnicodeError:
            raise InvalidAuthentication(
                "Invalid token header. Token string should not contain invalid characters.",
                code=ErrorCodes.access_token_invalid,
            )

        user_id = decoded_token["user"]
        try:
            user = CustomUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise InvalidAuthentication("No such user")

        return (user, token)

    @staticmethod
    def generate_jwt_token(user: CustomUser) -> str:
        app_config = apps.get_app_config("account")
        expiration_date = datetime.now() + timedelta(days=60)
        payload = {
            "user": user.id,
            "aud": app_config.BACKEND_JWT_AUD,
            "exp": expiration_date,
        }
        token = encode(payload, app_config.BACKEND_JWT_SECRET, algorithm="HS256")
        return token
