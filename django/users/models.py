from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    """
    Custom User model
    """

    # Add additional fields in here
    # https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#substituting-a-custom-user-model
    USERNAME_FIELD = 'email'
