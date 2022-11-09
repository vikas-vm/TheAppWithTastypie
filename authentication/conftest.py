import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_data():
    test_user = User.objects.create_user(
        email='test_email@mail.com',
        password='test_password',
        first_name='test_first_name',
        last_name='test_last_name',)
    return test_user
