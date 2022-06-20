from django.db.models import (
    CharField,
    IntegerField,
    DateField,
    BooleanField,
    PROTECT,
    ForeignKey,
)

from django.core.validators import MinLengthValidator
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from api.models.go_electric_rebate_application import GoElectricRebateApplication


class GoElectricRebate(TimeStampedModel):
    application = ForeignKey(
        GoElectricRebateApplication, on_delete=PROTECT, blank=True, null=True
    )
    drivers_licence = CharField(
        max_length=8, unique=True, validators=[MinLengthValidator(7)]
    )
    last_name = CharField(max_length=250, unique=False)
    expiry_date = DateField()
    rebate_max_amount = IntegerField(default=0)
    rebate_state = BooleanField(default=False)
