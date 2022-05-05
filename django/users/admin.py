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
        "username",
        "identity_provider",
        "display_name",
        "email",
        "is_staff",
        "is_superuser",
    ]


admin.site.register(ITVRUser, CustomUserAdmin)
