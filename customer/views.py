from .models import Customer, CustomerAddress, Cart, PaymentMethod, PaymentStatus, OrderStatus, Order
from django.urls import re_path
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpBadRequest, HttpNotFound
from authentication.jwt_auth import JWTAuthorization
from tastypie.serializers import Serializer
from tastypie import fields
import json
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomerResource(ModelResource):
    id = fields.IntegerField(attribute='id', readonly=True)

    class Meta:
        queryset = Customer.objects.all()
        resource_name = 'customer'
        authorization = JWTAuthorization()
        authentication = JWTAuthorization()
        serializer = Serializer(formats=['json'])
        allowed_methods = []
        list_allowed_methods = []
        detail_allowed_methods = []
        always_return_data = True

    def prepend_urls(self):
        return [
            re_path(r"^(?P<resource_name>%s)/detail%s$" %
                    (self._meta.resource_name, trailing_slash()), self.wrap_view('detail'), name="api_detail"),
            re_path(r"^(?P<resource_name>%s)/add_or_update_detail%s$" %
                    (self._meta.resource_name, trailing_slash()), self.wrap_view('add_or_update_detail'), name="api_add_or_update_detail"),
        ]

    def detail(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        customer = Customer.objects.filter(user=request.user).first()

        data = {
            'id': request.user.id,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': customer.phone if customer else None,
            'gender': customer.gender if customer else None,
            'dob': customer.dob if customer else None,
        }

        return self.create_response(request, data)

    def add_or_update_detail(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        customer = Customer.objects.filter(user=request.user).first()
        body = json.loads(request.body.decode('utf-8'))
        # print(customer)
        if customer:
            if body.get('phone'):
                customer.phone = body.get('phone')
            if body.get('dob'):
                customer.dob = body.get('dob')
            if body.get('gender'):
                customer.gender = body.get('gender')
            customer.save()
        else:
            customer = Customer(
                user=request.user
            )
            if body.get('phone'):
                customer.phone = body.get('phone')
            if body.get('dob'):
                customer.dob = body.get('dob')
            if body.get('gender'):
                customer.gender = body.get('gender')
            customer.save()

        user = request.user
        fields = body.keys()
        if bool({'first_name', 'last_name'}.intersection(fields)):
            if body.get('first_name'):
                user.first_name = body.get('first_name')
            if body.get('last_name'):
                user.last_name = body.get('last_name')
            user.save()

        data = {
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': customer.phone,
            'dob': customer.dob,
            'gender': customer.gender
        }
        return self.create_response(request, data)


class CustomerAddressResource(ModelResource):
    id = fields.IntegerField(attribute='id', readonly=True)

    class Meta:
        queryset = CustomerAddress.objects.all()
        resource_name = 'customer_address'
        authorization = JWTAuthorization()
        authentication = JWTAuthorization()
        serializer = Serializer(formats=['json'])
        # allowed_methods = []
        # list_allowed_methods = []
        # detail_allowed_methods = []
        always_return_data = True

    def obj_get(self, bundle, **kwargs):
        return CustomerAddress.objects.get(id=kwargs['pk'], customer__user=bundle.request.user)

    def obj_create(self, bundle, **kwargs):
        bundle.data['customer'] = Customer.objects.get(
            user=bundle.request.user)
        return super(CustomerAddressResource, self).obj_create(bundle, **kwargs)

    def obj_get_list(self, bundle, **kwargs):
        return CustomerAddress.objects.filter(customer__user=bundle.request.user)

    def obj_delete(self, bundle, **kwargs):
        return CustomerAddress.objects.get(id=kwargs['pk'], customer__user=bundle.request.user).delete()
