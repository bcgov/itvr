from shortuuid.django_fields import ShortUUIDField
from django.conf import settings
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
from ..models import GoElectricRebateApplication


class rebate_historical(TimeStampedModel):
    id = ShortUUIDField(length=16, primary_key=True, editable=False)
    application_id = ForeignKey(GoElectricRebateApplication, on_delete=PROTECT)
    drivers_licence = CharField(
        max_length=8, unique=False, validators=[MinLengthValidator(7)]
    )
    last_name = CharField(max_length=250, unique=False)
    expiry_date = DateField()
    rebate_max_amount = IntegerField(default=0)
    rebate_state = BooleanField(default=False)
