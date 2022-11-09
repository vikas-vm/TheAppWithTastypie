import pytest
from rest_framework.test import APIClient
from .models import Merchant

client = APIClient()


@pytest.mark.django_db
def test_add_merchant(user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Merchant1",
        "phone": "9098786798",
        "email": "testmail@mail.com"
    }
    response = client.post('/api/merchants/', payload)
    assert response.status_code == 201
    assert Merchant.objects.count() == 1
    assert Merchant.objects.get().name == payload['name']


@pytest.mark.django_db
def test_add_merchant_with_empty_body(user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {}
    response = client.post('/api/merchants/', payload)
    assert response.status_code == 400
    assert Merchant.objects.count() == 0
    assert response.data['name'][0] == 'This field is required.'
    assert response.data['phone'][0] == 'This field is required.'
    assert response.data['email'][0] == 'This field is required.'


@pytest.mark.django_db
def test_update_merchant(user_token, add_merchant):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Merchant1_updated",
        "phone": "9098786798",
        "email": "testmail@mail.com"
    }
    response = client.put('/api/merchants/'+str(add_merchant.id)+'/', payload)
    assert response.status_code == 200
    assert Merchant.objects.count() == 1
    assert Merchant.objects.get().name == payload['name']


@pytest.mark.django_db
def test_update_merchant_missing_body_field(user_token, add_merchant):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Merchant1_updated",
        "phone": "9098786798"
    }
    response = client.put('/api/merchants/'+str(add_merchant.id)+'/', payload)
    assert response.status_code == 400
    assert response.data['email'][0] == 'This field is required.'


@pytest.mark.django_db
def test__partial_update_merchant(user_token, add_merchant):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Merchant1_updated",
        "phone": "9098786798"
    }
    response = client.patch(
        '/api/merchants/'+str(add_merchant.id)+'/', payload)
    assert response.status_code == 200
    assert Merchant.objects.count() == 1
    assert Merchant.objects.get().name == payload['name']


@pytest.mark.django_db
def test_get_merchant(user_token, add_merchant):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    response = client.get('/api/merchants/'+str(add_merchant.id)+'/')
    assert response.status_code == 200
    assert response.data['name'] == add_merchant.name
    assert response.data['phone'] == add_merchant.phone
    assert response.data['email'] == add_merchant.email


@pytest.mark.django_db
def test_get_merchant_list(user_token, add_merchant):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    response = client.get('/api/merchants/')
    assert response.status_code == 200
    assert response.data[0]['name'] == add_merchant.name
    assert response.data[0]['phone'] == add_merchant.phone
    assert response.data[0]['email'] == add_merchant.email


@pytest.mark.django_db
def test_delete_merchant(user_token, add_merchant):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    response = client.delete('/api/merchants/'+str(add_merchant.id)+'/')
    assert response.status_code == 204
    assert Merchant.objects.count() == 0
