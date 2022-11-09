import pytest
from rest_framework.test import APIClient
from .models import Store

client = APIClient()


@pytest.mark.django_db
def test_add_store(add_merchant, user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Store1",
        "address": "Address1",
        "city": "City1",
        "state": "State1",
        "country": "Country1",
        "pincode": "123456",
        "merchant": add_merchant.id
    }
    response = client.post('/api/stores/', payload)
    assert response.status_code == 201
    assert Store.objects.count() == 1
    assert Store.objects.get().name == payload['name']


@pytest.mark.django_db
def test_add_store_with_missing_body(add_merchant, user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Store1",
        "address": "Address1",
        "city": "City1",
        "state": "State1",
        "pincode": "123456",
        "merchant": add_merchant.id
    }
    response = client.post('/api/stores/', payload)
    assert response.status_code == 400
    assert Store.objects.count() == 0
    assert response.data['country'][0] == 'This field is required.'


@pytest.mark.django_db
def test_add_store_with_empty_body(add_merchant, user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
    }
    response = client.post('/api/stores/', payload)
    assert response.status_code == 400
    assert Store.objects.count() == 0
    assert response.data['name'][0] == 'This field is required.'
    assert response.data['address'][0] == 'This field is required.'
    assert response.data['city'][0] == 'This field is required.'
    assert response.data['state'][0] == 'This field is required.'
    assert response.data['country'][0] == 'This field is required.'
    assert response.data['pincode'][0] == 'This field is required.'
    assert response.data['merchant'][0] == 'This field is required.'


@pytest.mark.django_db
def test_update_store(add_store, user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Store1_updated",
        "address": "Address1",
        "city": "City1",
        "state": "State1",
        "country": "Country1",
        "pincode": "123456",
        "merchant": add_store.merchant.id
    }
    response = client.put('/api/stores/'+str(add_store.id)+'/', payload)
    assert response.status_code == 200
    assert Store.objects.count() == 1
    assert Store.objects.get().name == payload['name']


@pytest.mark.django_db
def test_update_store_with_missing_body(add_store, user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Store1_updated",
        "address": "Address1",
        "city": "City1",
        "country": "Country1",
        "pincode": "123456",
        "merchant": add_store.merchant.id
    }
    response = client.put('/api/stores/'+str(add_store.id)+'/', payload)
    assert response.status_code == 400
    assert Store.objects.count() == 1
    assert response.data['state'][0] == 'This field is required.'
    assert Store.objects.get().name == add_store.name


@pytest.mark.django_db
def test_update_store_with_empty_body(add_store, user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
    }
    response = client.put('/api/stores/'+str(add_store.id)+'/', payload)
    assert response.status_code == 400
    assert Store.objects.count() == 1
    assert response.data['name'][0] == 'This field is required.'
    assert response.data['address'][0] == 'This field is required.'
    assert response.data['city'][0] == 'This field is required.'
    assert response.data['state'][0] == 'This field is required.'
    assert response.data['country'][0] == 'This field is required.'
    assert response.data['pincode'][0] == 'This field is required.'
    assert response.data['merchant'][0] == 'This field is required.'
    assert Store.objects.get().name == add_store.name
