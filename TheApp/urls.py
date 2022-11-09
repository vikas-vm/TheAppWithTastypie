from django.contrib import admin
from django.urls import path, include
from .apis import v1_api
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(v1_api.urls)),
]
