from .models import User
from django.urls import re_path
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from tastypie.http import HttpUnauthorized, HttpForbidden
from .jwt_auth import JWTAuthorization


class AuthResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['post']
        list_allowed_methods = []
        detail_allowed_methods = []
        resource_name = 'auth'

    def prepend_urls(self):
        return [
            re_path(r"^(?P<resource_name>%s)/token%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('token'), name="api_token"),

        ]

    def token(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        # self.is_authenticated(request)
        self.throttle_check(request)

        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        email = data.get('email', '')
        password = data.get('password', '')

        user = User.objects.filter(email=email)

        if user.exists():
            user = user.first()
        else:
            return self.create_response(request, {
                'success': False,
                'message': 'User does not exist'
            }, HttpUnauthorized)

        if user:
            if not user.check_password(password):
                return self.create_response(request, {
                    'success': False,
                    'message': 'Password is incorrect'
                }, HttpUnauthorized)
            if user.is_active:
                data = {
                    'token': user.generate_token(),
                    'user_id': user.pk,
                    'email': user.email
                }
                return self.create_response(request, data)
            else:
                return self.create_response(request, {'error_message': 'Sorry, this account has been disabled.'}, HttpForbidden)
        else:
            return self.create_response(request, {'error_message': 'Invalid login credentials.'}, HttpUnauthorized)
