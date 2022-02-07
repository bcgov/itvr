from django.db.models import CharField, IntegerField
from auditable.models import Auditable


class IncomeVerification(Auditable):
    sin = CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
    last_name = CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
    first_name = CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
    date_of_birth = IntegerField(
        blank=True,
        null=True
    )
    tax_year = IntegerField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'income_verification'
