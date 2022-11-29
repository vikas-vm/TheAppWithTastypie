import jwt
from django.conf import settings
from tastypie.authorization import DjangoAuthorization
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthorization(DjangoAuthorization):
    def is_authenticated(self, request, **kwargs):
        request.user = None
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token is None:
            return False
        else:
            token = token.split(' ')[1]
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['id'])
            if user.is_active and user.user_type == 'MERCHANT':
                request.user = user
                return True
            else:
                return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.DecodeError:
            return False
        except User.DoesNotExist:
            return False

    def get_identifier(self, request):
        return request.user.email


class CustomerJWTAuthorization(DjangoAuthorization):
    def is_authenticated(self, request, **kwargs):
        request.user = None
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token is None:
            return False
        else:
            token = token.split(' ')[1]
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['id'])
            if user.is_active and user.user_type == 'CUSTOMER':
                request.user = user
                return True
            else:
                return False
        except jwt.ExpiredSignatureError:
            return False
        except jwt.DecodeError:
            return False
        except User.DoesNotExist:
            return False

    def get_identifier(self, request):
        return request.user.email
