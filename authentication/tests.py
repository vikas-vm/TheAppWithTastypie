import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import User


client = APIClient()
Users = get_user_model()


@pytest.mark.django_db
def test_user_registration():
    payload = {
        'email': 'test_email@mail.com',
        'password1': 'test_password',
        'password2': 'test_password',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
    }
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.get().email == payload['email']


@pytest.mark.django_db
def test_register_user_with_no_first_name():
    payload = {
        'email': 'test_email@mail.com',
        'password1': 'test_password',
        'password2': 'test_password',
        'last_name': 'test_last_name',
    }
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 400
    assert User.objects.count() == 0
    assert response.data['first_name'] == ['This field is required.']


@pytest.mark.django_db
def test_register_user_with_no_last_name():
    payload = {
        'email': 'test_email@mail.com',
        'password1': 'test_password',
        'password2': 'test_password',
        'first_name': 'test_first_name',
    }
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 400
    assert User.objects.count() == 0
    assert response.data['last_name'] == ['This field is required.']


@pytest.mark.django_db
def test_register_user_with_no_email():
    payload = {
        'password1': 'test_password',
        'password2': 'test_password',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
    }
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 400
    assert User.objects.count() == 0
    assert response.data['email'] == ['This field is required.']


@pytest.mark.django_db
def test_register_user_with_no_password1():
    payload = {
        'email': 'test_email@mail.com',
        'password2': 'test_password',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
    }
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 400
    assert User.objects.count() == 0
    assert response.data['password1'] == ['This field is required.']


@pytest.mark.django_db
def test_register_user_with_no_password2():
    payload = {
        'email': 'test_email@mail.com',
        'password1': 'test_password',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
    }
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 400
    assert User.objects.count() == 0
    assert response.data['password2'] == ['This field is required.']


@pytest.mark.django_db
def test_register_user_with_invalid_email():
    payload = {
        'email': 'test_email',
        'password1': 'test_password',
        'password2': 'test_password',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
    }
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 400
    assert User.objects.count() == 0
    assert response.data['email'] == ['Enter a valid email address.']


@pytest.mark.django_db
def test_register_user_with_existing_email():
    payload = {
        'email': 'test_email@mail.com',
        'password1': 'test_password',
        'password2': 'test_password',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
    }
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 201
    assert User.objects.count() == 1
    assert User.objects.get().email == payload['email']
    response = client.post('/api/auth/register/', payload)
    assert response.status_code == 400
    assert User.objects.count() == 1
    assert response.data['email'] == [
        'User with this email already exists.']


@pytest.mark.django_db
def test_user_login(user_data):
    payload = {
        'email': 'test_email@mail.com',
        'password': 'test_password'
    }
    response = client.post('/api/auth/token/', payload)
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_user_login_with_wrong_credential(user_data):
    payload = {
        'email': 'test_email@mail.com',
        'password': 'wrong_password'
    }
    response = client.post('/api/auth/token/', payload)
    assert response.status_code == 401
    assert 'error' in response.data
    assert response.data['error'] == 'Invalid Credentials'


@pytest.mark.django_db
def test_user_login_with_wrong_email(user_data):
    payload = {
        'email': 'wrong_email@mail.com',
        'password': 'test_password'
    }
    response = client.post('/api/auth/token/', payload)
    assert response.status_code == 401
    assert 'error' in response.data
    assert response.data['error'] == 'Invalid Credentials'
