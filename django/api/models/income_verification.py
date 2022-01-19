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

    class Meta:
        db_table = "income_verification"