from django.db.models import CharField, IntegerField, BooleanField
from auditable.models import Auditable


class IncomeVerification2(Auditable):
    household = BooleanField(
        default=False
    )

    # TBD: Maybe just add email address if that's all we need.
    spouse_id = IntegerField(
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'income_verification'
