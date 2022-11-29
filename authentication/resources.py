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
        allowed_methods = []
        list_allowed_methods = []
        detail_allowed_methods = []
        resource_name = 'auth'

    def prepend_urls(self):
        return [
            re_path(r"^(?P<resource_name>%s)/token%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('token'), name="api_token"),
            re_path(r"^(?P<resource_name>%s)/register%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('register'), name="api_register"),

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
                if not user.user_type == 'MERCHANT':
                    return self.create_response(request, {
                        'success': False,
                        'message': 'You are not authorized to access Merchant Portal'
                    }, HttpForbidden)

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

    def register(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        # self.is_authenticated(request)
        self.throttle_check(request)

        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        required_fields = ['email', 'password']
        missing_data = {}
        is_missing_data = False
        for field in required_fields:
            if not data.get(field, ''):
                missing_data[field] = 'This field is required'
                is_missing_data = True
        if is_missing_data:
            return self.create_response(request, missing_data, HttpUnauthorized)

        email = data.get('email', '')
        password = data.get('password', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        user = User.objects.filter(email=email)

        if user.exists():
            return self.create_response(request, {
                'success': False,
                'message': 'User already exists'
            }, HttpUnauthorized)
        else:
            user = User(
                email=email, first_name=first_name, last_name=last_name)
            user.user_type = 'MERCHANT'
            user.set_password(password)
            user.save()

            return self.create_response(request, {
                'success': True,
                'message': 'User created successfully',
                'data': {
                    'token': user.generate_token(),
                    'user_id': user.pk,
                    'email': user.email
                }
            })


class CustomerAuthResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = []
        list_allowed_methods = []
        detail_allowed_methods = []
        resource_name = 'auth'

    def prepend_urls(self):
        return [
            re_path(r"^(?P<resource_name>%s)/token%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('token'), name="api_token"),
            re_path(r"^(?P<resource_name>%s)/register%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('register'), name="api_register"),

        ]

    def token(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
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
                if not user.user_type == 'CUSTOMER':
                    return self.create_response(request, {
                        'success': False,
                        'message': 'You are not authorized to access Customer Portal'
                    }, HttpForbidden)

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

    def register(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        self.throttle_check(request)

        data = self.deserialize(request, request.body, format=request.META.get
                                ('CONTENT_TYPE', 'application/json'))
        required_fields = ['email', 'password']
        missing_data = {}
        is_missing_data = False
        for field in required_fields:
            if not data.get(field, ''):
                missing_data[field] = 'This field is required'
                is_missing_data = True
        if is_missing_data:
            return self.create_response(request, missing_data, HttpUnauthorized)

        email = data.get('email', '')
        password = data.get('password', '')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')

        user = User.objects.filter(email=email)

        if user.exists():
            return self.create_response(request, {
                'success': False,
                'message': 'User already exists'
            }, HttpUnauthorized)
        else:
            user = User(
                email=email, first_name=first_name, last_name=last_name)
            user.user_type = 'CUSTOMER'
            user.set_password(password)
            user.save()

            return self.create_response(request, {
                'success': True,
                'message': 'User created successfully',
                'data': {
                    'token': user.generate_token(),
                    'user_id': user.pk,
                    'email': user.email
                }
            })
