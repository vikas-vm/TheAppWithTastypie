import pytest
from rest_framework.test import APIClient
from .models import Category

client = APIClient()


@pytest.mark.django_db
def test_add_category(user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Category1"
    }
    response = client.post('/api/categories/', payload)
    assert response.status_code == 201
    assert Category.objects.count() == 1
    assert Category.objects.get().name == payload['name']


@pytest.mark.django_db
def test_add_category_with_empty_body(user_token):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {}
    response = client.post('/api/categories/', payload)
    assert response.status_code == 400
    assert Category.objects.count() == 0
    assert response.data['name'][0] == 'This field is required.'


@pytest.mark.django_db
def test_add_category_with_parent(user_token, add_category):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Category2",
        "parent": add_category.id
    }
    response = client.post('/api/categories/', payload)
    assert response.status_code == 201
    assert Category.objects.count() == 2
    assert Category.objects.get(name=payload['name']).parent == add_category


@pytest.mark.django_db
def test_update_category(user_token, add_category):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Category1_updated"
    }
    response = client.put('/api/categories/'+str(add_category.id)+'/', payload)
    assert response.status_code == 200
    assert Category.objects.count() == 1
    assert Category.objects.get().name == payload['name']


@pytest.mark.django_db
def test_update_category_with_parent(user_token, add_category):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_token)
    payload = {
        "name": "Category1_updated",
        "parent": add_category.id
    }
    response = client.put('/api/categories/'+str(add_category.id)+'/', payload)
    assert response.status_code == 200
    assert Category.objects.count() == 1
    assert Category.objects.get().name == payload['name']
    assert Category.objects.get().parent == add_category
