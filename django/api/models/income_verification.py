<<<<<<< HEAD
from django.db import models

class IncomeVerification():

    create_timestamp = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    update_timestamp = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True
    )   

    sin = models.CharField(
=======
from django.db.models import CharField, IntegerField
from auditable.models import Auditable


class IncomeVerification(Auditable):
    sin = CharField(
>>>>>>> upstream/release-0.1.0
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
<<<<<<< HEAD

    surname = models.CharField(
=======
    last_name = CharField(
>>>>>>> upstream/release-0.1.0
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
<<<<<<< HEAD

    first_name = models.CharField(
=======
    first_name = CharField(
>>>>>>> upstream/release-0.1.0
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
<<<<<<< HEAD

    date_of_birth = models.IntegerField(
        blank=True,
        null=True
    )

    tax_year = models.IntegerField(
=======
    date_of_birth = IntegerField(
        blank=True,
        null=True
    )
    tax_year = IntegerField(
>>>>>>> upstream/release-0.1.0
        blank=True,
        null=True
    )

    class Meta:
<<<<<<< HEAD
        db_table = "income_verification"


# SIN (Social Insurance Number) - encrypted (Richard to provide info/link)
# Surname (30 character limit)
# First name (30 character limit)
# Date of birth (yyyymmdd) (numeric 8)
# Tax year (numeric 4)
=======
        db_table = 'income_verification'
>>>>>>> upstream/release-0.1.0
