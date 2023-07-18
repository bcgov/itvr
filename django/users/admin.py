from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

ITVRUser = get_user_model()


@admin.register(ITVRUser)
class CustomUserAdmin(UserAdmin):
    model = ITVRUser
    actions = None
    list_filter = []
    list_display = [
        "username",
        "email",
        "is_staff",
        "is_superuser",
    ]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        if not request.user.is_superuser:
            return (
                (None, {"fields": ("username", "password")}),
                (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
                (
                    _("Permissions"),
                    {
                        "fields": (
                            "is_active",
                            "is_staff",
                            "groups",
                        ),
                    },
                ),
                (_("Important dates"), {"fields": ("last_login", "date_joined")}),
            )
        return super().get_fieldsets(request, obj)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return ITVRUser.objects.filter(identity_provider="")
        return ITVRUser.objects.filter(identity_provider="").filter(is_superuser=False)
