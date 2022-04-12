from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class ITVRUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class ITVRUser(AbstractUser):
    """
    Custom User model

    User Identifier is mandatory, that's who the person is.
    It's the one value that will never change.

    On 95% of the integrations, I'd heavily recommend we use
    “Authentication Transaction Identifier”.
    Helps with the actual time a citizen logs in or if you need
    to make any troubleshooting with us, it's nice to have a
    common element on both sides to look at.

    The others are used infrequently.
    Some examples would be, if you had lots of IDPs
    (like our Federal Gov't integrations also have other provinces)
    and you needed to know it was from BC Services Card (IAS),
    you'd probably want the Authoritative Party Name.
    """

    # Add additional fields in here
    # https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#substituting-a-custom-user-model

    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = ITVRUserManager()
