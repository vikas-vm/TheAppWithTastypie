import pytest
from django.contrib.auth import get_user_model
from .models import Merchant, Store, Category, Item

from authentication.conftest import user_data
from rest_framework.test import APIClient
client = APIClient()

User = get_user_model()


@pytest.fixture
def user_token(user_data):
    token_pair = client.post('/api/auth/token/', {
        'email': 'test_email@mail.com',
        'password': 'test_password',
    })
    token = token_pair.data['access']
    return token


@pytest.fixture
def add_merchant():
    merchant = Merchant.objects.create(
        name='Merchant1',
        phone='9098786798',
        email="test_merchant_email@mail.com",
    )
    return merchant


@pytest.fixture
def add_store(add_merchant):
    store = Store.objects.create(
        name='Store1',
        address='Address1',
        city='City1',
        state='State1',
        pincode='123456',
        merchant=add_merchant,
    )
    return store


@pytest.fixture
def add_category():
    category = Category.objects.create(
        name='Category1',
    )
    return category


@pytest.fixture
def add_item(add_category, add_store):
    item = Item.objects.create(
        name="item1",
        price=600,
        store=add_store,
        category=add_category,
        description="this is description",
        discount=10,
        discount_type="flat"
    )
    return item
