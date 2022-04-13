from django.contrib.auth.models import AbstractBaseUser
from django.db.models import (
    CharField,
    TextField,
)


class Applicant(AbstractBaseUser):
    # bceid-basic or for BC Services Card it is “IAS” at this time.
    identity_provider = CharField(max_length=11)

    # bceid-basic uuid4
    # bc services card This is also known as the Directed Identifier (DID),
    # and may be up to 255 characters.
    sub = CharField(max_length=255)

    display_name = TextField()

    class Meta:
        db_table = "applicants"
