from unicodedata import category
from rest_framework.serializers import ModelSerializer
from .models import Merchant, Store, Item, Category


class MerchantSerializer(ModelSerializer):
    class Meta:
        model = Merchant
        exclude = ['created_by', 'updated_by']


class StoreSerializer(ModelSerializer):
    class Meta:
        model = Store
        exclude = ['created_by', 'updated_by']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ['created_by', 'updated_by']


class ItemSerializer(ModelSerializer):
    category_detail = CategorySerializer(read_only=True, source='category')

    class Meta:
        model = Item
        exclude = ['created_by', 'updated_by']
