from rest_framework import routers

from .apis import MerchantViewset, StoreViewset, CategoryViewset, ItemViewset


router = routers.DefaultRouter()
router.register('merchants', MerchantViewset)
router.register('stores', StoreViewset)
router.register('categories', CategoryViewset)
router.register('items', ItemViewset)
