import pytest
from rest_framework.test import APIClient
from .models import Item

client = APIClient()


@pytest.mark.django_db
def test_add_item(user_token, add_store, add_category):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "items",
        "price": "600",
        "discount": 10,
        "discount_type": "percent",
        "store": add_store.id,
        "category": add_category.id,
        "description": "this is description",
    }
    response = client.post('/api/items/', payload)
    assert response.status_code == 201
    assert Item.objects.count() == 1
    assert Item.objects.get().name == payload['name']


@pytest.mark.django_db
def test_add_item_with_empty_body(user_token, add_store, add_category):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {}
    response = client.post('/api/items/', payload)
    assert response.status_code == 400
    assert Item.objects.count() == 0
    assert response.data['name'][0] == 'This field is required.'
    assert response.data['price'][0] == 'This field is required.'
    assert response.data['store'][0] == 'This field is required.'
    assert response.data['category'][0] == 'This field is required.'


@pytest.mark.django_db
def test_add_item_with_invalid_value_for_choice_filed_discount_type(user_token, add_store, add_category):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "items",
        "price": "600",
        "discount": 10,
        "discount_type": "invalid",
        "store": 1,
        "category": 1,
        "description": "this is description",
    }
    response = client.post('/api/items/', payload)
    assert response.status_code == 400
    assert Item.objects.count() == 0
    assert response.data['discount_type'][0] == '"invalid" is not a valid choice.'


@pytest.mark.django_db
def test_update_item(user_token, add_item, add_store, add_category):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "items_updated",
        "price": "600",
        "discount": 10,
        "discount_type": "percent",
        "description": "this is description",
        "store": add_store.id,
        "category": add_category.id,
    }
    response = client.put('/api/items/'+str(add_item.id)+'/', payload)
    print(response.data)
    assert response.status_code == 200
    assert Item.objects.count() == 1
    assert Item.objects.get().name == payload['name']


@pytest.mark.django_db
def test_update_item_with_missing_required_field(user_token, add_item):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "items_updated",
        "price": "600",
        "discount": 10,
        "discount_type": "percent",
        "description": "this is description",
    }
    response = client.put('/api/items/'+str(add_item.id)+'/', payload)
    assert response.status_code == 400
    assert Item.objects.count() == 1
    assert response.data['store'][0] == 'This field is required.'
    assert response.data['category'][0] == 'This field is required.'


@pytest.mark.django_db
def test_partial_update_item(user_token, add_item):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "items_updated"
    }
    response = client.patch('/api/items/'+str(add_item.id)+'/', payload)
    assert response.status_code == 200
    assert Item.objects.count() == 1
    assert Item.objects.get().name == payload['name']


@pytest.mark.django_db
def test_delete_item(user_token, add_item):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    response = client.delete('/api/items/'+str(add_item.id)+'/')
    assert response.status_code == 204
    assert Item.objects.count() == 0
