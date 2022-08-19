from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ITVRUserCreationForm, ITVRUserChangeForm

ITVRUser = get_user_model()


@admin.register(ITVRUser)
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

    def get_queryset(self, request):
        is_superuser = request.user.is_superuser
        return super().get_queryset(request) if is_superuser else super().get_queryset(request).filter(is_staff=True)

