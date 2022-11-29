from .models import Merchant, Store, Category, Item
from django.urls import re_path
from tastypie.utils import trailing_slash
from tastypie.resources import ModelResource
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpBadRequest, HttpNotFound
from authentication.jwt_auth import JWTAuthorization
from tastypie.serializers import Serializer
from tastypie import fields


class MerchantModelResource(ModelResource):
    id = fields.IntegerField(attribute='id', readonly=True)
    created_at = fields.DateTimeField(attribute='created_at', readonly=True)
    updated_at = fields.DateTimeField(attribute='updated_at', readonly=True)

    class Meta:
        queryset = Merchant.objects.all()
        allowed_methods = []
        list_allowed_methods = []
        detail_allowed_methods = []
        resource_name = 'profile'
        authentication = JWTAuthorization()
        authorization = JWTAuthorization()
        serializer = Serializer()

    def prepend_urls(self):
        return [
            re_path(r"^(?P<resource_name>%s)/detail%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('detail'), name="api_detail"),
            re_path(r"^(?P<resource_name>%s)/add_or_update_detail%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('add_or_update_detail'), name="api_add_or_update_detail"),

        ]

    def detail(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        merchant = Merchant.objects.filter(user=request.user)
        if merchant.exists():
            merchant = merchant.first()
        else:
            return self.create_response(request, {
                'success': False,
                'message': 'Merchant detail not found',
            }, HttpNotFound)

        data = {
            'id': request.user.id,
            'name': merchant.name,
            'address1': merchant.address1,
            'address2': merchant.address2,
            'city': merchant.city,
            'state': merchant.state,
            'zip': merchant.zip,
            'phone': merchant.phone,
            'venue_id': merchant.venue_id,
            'registered_id': merchant.registered_id,
        }
        return self.create_response(request, {
            'success': True,
            'message': 'Merchant details',
            'data': data
        })

    def add_or_update_detail(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        merchant = Merchant.objects.filter(user=request.user)
        if merchant.exists():
            merchant = merchant.first()
            if data.get('name'):
                merchant.name = data.get('name')
            if data.get('address1'):
                merchant.address1 = data.get('address1')
            if data.get('address2'):
                merchant.address2 = data.get('address2')
            if data.get('city'):
                merchant.city = data.get('city')
            if data.get('state'):
                merchant.state = data.get('state')
            if data.get('zip'):
                merchant.zip = data.get('zip')
            if data.get('phone'):
                merchant.phone = data.get('phone')
            if data.get('venue_id'):
                merchant.venue_id = data.get('venue_id')
            if data.get('registered_id'):
                merchant.registered_id = data.get('registered_id')
            merchant.save()
        else:
            required_fields = ['name', 'address1',
                               'city', 'state', 'zip', 'phone']
            missing_data = {}
            is_missing = False
            for field in required_fields:
                if not data.get(field):
                    missing_data[field] = 'This field is required'
                    is_missing = True
            if is_missing:
                return self.create_response(request, {
                    'success': False,
                    'message': 'Missing data',
                    'data': missing_data
                }, HttpBadRequest)

            merchant = Merchant.objects.create(
                user=request.user,
                name=data.get('name', ''),
                address1=data.get('address1', ''),
                address2=data.get('address2', ''),
                city=data.get('city', ''),
                state=data.get('state', ''),
                zip=data.get('zip', ''),
                phone=data.get('phone', ''),
                venue_id=data.get('venue_id', ''),
                registered_id=data.get('registered_id', ''),
            )
        data = {
            'id': merchant.id,
            'name': merchant.name,
            'address1': merchant.address1,
            'address2': merchant.address2,
            'city': merchant.city,
            'state': merchant.state,
            'zip': merchant.zip,
            'phone': merchant.phone,
            'venue_id': merchant.venue_id,
            'registered_id': merchant.registered_id,
        }
        return self.create_response(request, {
            'success': True,
            'message': 'Merchant details',
            'data': data
        })


class StoreModelResource(ModelResource):
    id = fields.IntegerField(attribute='id', readonly=True)
    created_at = fields.DateTimeField(attribute='created_at', readonly=True)
    updated_at = fields.DateTimeField(attribute='updated_at', readonly=True)
    # items = fields.ToManyField(
    #     'merchant.resources.ItemModelResource', 'items', readonly=True, null=True)

    class Meta:
        queryset = Store.objects.all()
        resource_name = 'store'
        authentication = JWTAuthorization()
        authorization = JWTAuthorization()
        serializer = Serializer()
        always_return_data = True

    def prepend_urls(self):
        return [
            re_path(r"^(?P<resource_name>%s)/(?P<store_id>\d+)/items%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('items'), name="api_items"),
            re_path(r"^(?P<resource_name>%s)/(?P<store_id>\d+)/item/add%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('adding_item_to_store'), name="api_add_item"),
            re_path(r"^(?P<resource_name>%s)/(?P<store_id>\d+)/item/remove%s$" % (self._meta.resource_name,
                    trailing_slash()), self.wrap_view('remove_item_from_store'), name="api_remove_item"),
        ]

    def obj_get_list(self, bundle, **kwargs):
        return Store.objects.filter(merchant__user=bundle.request.user)

    def obj_get(self, bundle, **kwargs):
        return Store.objects.get(id=kwargs['pk'], merchant__user=bundle.request.user)

    def obj_create(self, bundle, **kwargs):
        bundle = super(StoreModelResource, self).obj_create(bundle, **kwargs)
        bundle.obj.merchant = Merchant.objects.get(user=bundle.request.user)
        bundle.obj.save()
        return bundle

    def obj_update(self, bundle, **kwargs):
        bundle = super(StoreModelResource, self).obj_update(bundle, **kwargs)
        bundle.obj.merchant = Merchant.objects.get(user=bundle.request.user)
        bundle.obj.save()
        return bundle

    def obj_delete(self, bundle, **kwargs):
        return Store.objects.get(id=kwargs['pk'], merchant__user=bundle.request.user).delete()

    def hydrate(self, bundle):
        bundle.obj.merchant = Merchant.objects.get(user=bundle.request.user)
        return bundle

    def items(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        store = Store.objects.filter(
            id=kwargs['store_id'], merchant__user=request.user)

        if store.exists():
            store = store.first()
        else:
            return self.create_response(request, {
                'success': False,
                'message': 'Store not found',
                'data': {}
            }, HttpNotFound)
        items = Item.objects.filter(store=store)
        data = []
        for item in items:
            data.append('/api/v1/item/%s/' % item.id)
        return self.create_response(request, {
            'success': True,
            'message': 'Store items',
            'data': data
        })

    def adding_item_to_store(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        store = Store.objects.filter(
            id=kwargs['store_id'], merchant__user=request.user)
        if store:
            store = store.first()
        else:
            return self.create_response(request, {
                'success': False,
                'message': 'Store not found',
                'data': {}
            }, HttpNotFound)
        if data.get('item'):
            # check if item is associated with less than 3 stores
            item = Item.objects.filter(
                id=data.get('item'),  store__isnull=False)
            item = Item.objects.filter(id=data.get(
                'item'), merchant=store.merchant)
            if item:
                item = item.first()
            else:
                return self.create_response(request, {
                    'success': False,
                    'message': 'Item not found for this merchant',
                    'data': {}
                }, HttpNotFound)
            item.store.add(store)
            item.save()
            return self.create_response(request, {
                'success': True,
                'message': 'Item added to store',
                'data': {}
            })
        else:
            return self.create_response(request, {
                'success': False,
                'message': 'Missing fields',
                'data': {
                    "item": "This field is required."
                }
            }, HttpBadRequest)

    def remove_item_from_store(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)
        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        store = Store.objects.filter(
            id=kwargs['store_id'], merchant__user=request.user)
        if store:
            store = store.first()
        else:
            return self.create_response(request, {
                'success': False,
                'message': 'Store not found',
                'data': {}
            }, HttpNotFound)
        if data.get('item'):
            item = Item.objects.filter(id=data.get(
                'item'), merchant=store.merchant)
            if item:
                item = item.first()
            else:
                return self.create_response(request, {
                    'success': False,
                    'message': 'Item not found for this merchant',
                    'data': {}
                }, HttpNotFound)
            if not item.store.filter(id=store.id).exists():
                return self.create_response(request, {
                    'success': False,
                    'message': 'Item not found in this store',
                    'data': {}
                }, HttpNotFound)
            item.store.remove(store)
            item.save()
            return self.create_response(request, {
                'success': True,
                'message': 'Item removed from store',
                'data': {}
            })
        else:
            return self.create_response(request, {
                'success': False,
                'message': 'Missing fields',
                'data': {
                    "item": "This field is required."
                }
            }, HttpBadRequest)


class CategoryModelResource(ModelResource):
    id = fields.IntegerField(attribute='id', readonly=True)
    created_at = fields.DateTimeField(attribute='created_at', readonly=True)
    updated_at = fields.DateTimeField(attribute='updated_at', readonly=True)
    parent = fields.ForeignKey(
        'self', 'parent', null=True, blank=True)

    class Meta:
        queryset = Category.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'patch']
        resource_name = 'category'
        authentication = JWTAuthorization()
        authorization = JWTAuthorization()
        serializer = Serializer()
        always_return_data = True
        read_only_fields = ['id', 'created_at', 'updated_at']


class ItemModelResource(ModelResource):
    id = fields.IntegerField(attribute='id', readonly=True)
    created_at = fields.DateTimeField(attribute='created_at', readonly=True)
    updated_at = fields.DateTimeField(attribute='updated_at', readonly=True)
    category = fields.ForeignKey(CategoryModelResource, 'category')
    store = fields.ToManyField(StoreModelResource, 'store', readonly=True)

    class Meta:
        queryset = Item.objects.all()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'patch']
        resource_name = 'item'
        authentication = JWTAuthorization()
        authorization = JWTAuthorization()
        serializer = Serializer()
        always_return_data = True

    def obj_get_list(self, bundle, **kwargs):
        return Item.objects.filter(merchant__user=bundle.request.user)

    def obj_get(self, bundle, **kwargs):
        return Item.objects.get(id=kwargs['pk'], merchant__user=bundle.request.user)

    def obj_create(self, bundle, **kwargs):
        bundle = super(ItemModelResource, self).obj_create(bundle, **kwargs)
        bundle.obj.merchant = Merchant.objects.get(user=bundle.request.user)
        bundle.obj.save()
        return bundle

    def obj_update(self, bundle, **kwargs):
        bundle = super(ItemModelResource, self).obj_update(bundle, **kwargs)
        bundle.obj.merchant = Merchant.objects.get(user=bundle.request.user)
        bundle.obj.save()
        return bundle

    def obj_delete(self, bundle, **kwargs):
        return Item.objects.get(id=kwargs['pk'], store__merchant__user=bundle.request.user).delete()

    def hydrate(self, bundle):
        bundle.obj.merchant = Merchant.objects.get(user=bundle.request.user)
        return bundle
