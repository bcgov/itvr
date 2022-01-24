from django.db import models


class IncomeVerification():
    sin = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
    last_name = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
    first_name = models.CharField(
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
    date_of_birth = models.IntegerField(
        blank=True,
        null=True
    )
    tax_year = models.IntegerField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'income_verification'
