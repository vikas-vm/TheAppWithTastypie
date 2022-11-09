from tastypie.api import Api

from authentication.resources import AuthResource
from merchant.resources import MerchantModelResource, StoreModelResource, CategoryModelResource, ItemModelResource

v1_api = Api(api_name='v1')
v1_api.register(AuthResource())
v1_api.register(MerchantModelResource())
v1_api.register(StoreModelResource())
v1_api.register(CategoryModelResource())
v1_api.register(ItemModelResource())
