from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ITVRUserCreationForm, ITVRUserChangeForm

ITVRUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = ITVRUserCreationForm
    form = ITVRUserChangeForm
    model = ITVRUser
    list_display = [
        "identity_provider",
        "sub",
        "display_name",
        "email",
        "username",
        "is_staff",
        "is_superuser",
    ]


if settings.DEBUG:
    admin.site.register(ITVRUser, CustomUserAdmin)
