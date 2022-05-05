from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models import (
    CharField,
    TextField,
)


class ITVRUser(AbstractUser):
    """
    ITVR User which can support BCeID and BC Services card logins
    """

    # Add additional fields in here
    # https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#substituting-a-custom-user-model

    # bceid-basic or for BC Services Card it is “IAS” at this time.
    identity_provider = CharField(
        _("identity provider"),
        max_length=11,
        help_text=_("Name of the identity provider through keycloak."),
    )

    # use sub from jwt token if keycloak user
    # bceid-basic uuid4
    # bc services card This is also known as the Directed Identifier (DID),
    # and may be up to 255 characters.
    username = CharField(
        _("username"),
        max_length=255,
        unique=True,
        help_text=_("Required. 255 characters or fewer."),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    display_name = TextField(
        _("display name"),
        help_text=_("Taken from the keycloak JWT."),
    )

    def __str__(self):
        return self.identity_provider + " " + self.display_name
