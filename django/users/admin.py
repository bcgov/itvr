from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ITVRUserCreationForm, ITVRUserChangeForm
from django.utils.translation import gettext as _

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

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            perm_fields = ('is_active', 'is_staff', 'groups')

        return [(None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]
