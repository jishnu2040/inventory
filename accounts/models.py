from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import timedelta

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)  # Set to False until email verification
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def token(self):
        refresh_token = RefreshToken.for_user(self)
        refresh_token.set_exp(lifetime=timedelta(days=7))  # Custom expiration time
        return {
            'refresh': str(refresh_token),
            'access': str(refresh_token.access_token)
        }

    @property
    def is_authenticated(self):
        return True
