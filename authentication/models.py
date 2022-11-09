from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from enum import Enum
import jwt
from datetime import datetime, timedelta
from django.conf import settings

# Create your models here.


class UserTypes(Enum):
    MERCHANT = 'MERCHANT'
    CUSTOMER = 'CUSTOMER'


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                _('Supergit@github.com:vikas-vm/TheAppWithTastypie.gituser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=150, blank=True, null=True, unique=True)
    user_type = models.CharField(
        max_length=50, choices=[(tag, tag.value) for tag in UserTypes])
    USERNAME_FIELD = 'email'
    is_active = models.BooleanField(default=True)
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = UserManager()

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'users'

    def generate_token(self):
        token = jwt.encode({
            'id': self.pk,
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow()
        }, settings.SECRET_KEY, algorithm='HS256')
        return token
