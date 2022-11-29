from django.contrib import admin
from django.urls import path, include
from .apis import v1_api, v1_api_customer
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(v1_api.urls)),
    path('api/', include(v1_api_customer.urls)),
]
