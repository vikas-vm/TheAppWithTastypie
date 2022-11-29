from tastypie.api import Api

from authentication.resources import AuthResource, CustomerAuthResource
from merchant.resources import MerchantModelResource, StoreModelResource, CategoryModelResource, ItemModelResource
from customer.views import CustomerResource

v1_api = Api(api_name='v1/merchant')
v1_api.register(AuthResource())
v1_api.register(MerchantModelResource())
v1_api.register(StoreModelResource())
v1_api.register(CategoryModelResource())
v1_api.register(ItemModelResource())

v1_api_customer = Api(api_name='v1')
v1_api_customer.register(CustomerAuthResource())
v1_api_customer.register(CustomerResource())
