from django.contrib import admin
from .models import Merchant, Store, Category

# Register your models here.
admin.site.register(Merchant)
admin.site.register(Store)
admin.site.register(Category)
