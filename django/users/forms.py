from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class ITVRUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = (
            "email",
            "username",
        )


class ITVRUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )
