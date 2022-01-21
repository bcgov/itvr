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
        blank=True,
        null=True,
        max_length=250,
        unique=False
    )
    surname = models.CharField(
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
