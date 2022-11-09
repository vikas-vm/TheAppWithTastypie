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
            if user.is_active:
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

    # def get_list(self, object_list, bundle):
    #     return object_list.filter(email=bundle.request.user.email)

    # def get_object_list(self, request):
    #     return super(JWTAuthorization, self).get_object_list(request).filter(email=request.user.email)

    # def read_list(self, object_list, bundle):
    #     return object_list.filter(email=bundle.request.user.email)

    # def read_detail(self, object_list, bundle):
    #     return bundle.obj.email == bundle.request.user.email

    # def create_list(self, object_list, bundle):
    #     return object_list.filter(email=bundle.request.user.email)

    # def create_detail(self, object_list, bundle):
    #     return bundle.obj.email == bundle.request.user.email

    # def update_list(self, object_list, bundle):
    #     return object_list.filter(email=bundle.request.user.email)

    # def update_detail(self, object_list, bundle):
    #     return bundle.obj.email == bundle.request.user.email

    # def delete_list(self, object_list, bundle):
    #     return object_list.filter(email=bundle.request.user.email)

    # def delete_detail(self, object_list, bundle):
    #     return bundle.obj.email == bundle.request.user.email

    # def apply_limits(self, request, object_list):
    #     return object_list.filter(email=request.user.email)

    # def authorized_read_list(self, object_list, bundle):
    #     return object_list.filter(email=bundle.request.user.email)

    # def authorized_read_detail(self, object_list, bundle):
    #     return bundle.obj.email == bundle.request.user.email

    # def authorized_create_list(self, object_list, bundle):
    #     return object_list.filter(email=bundle.request.user.email)

    # def authorized_create_detail(self, object_list, bundle):
    #     return bundle.obj.email == bundle.request.user.email

    # def authorized_update_list(self, object_list, bundle):
    #     return object
