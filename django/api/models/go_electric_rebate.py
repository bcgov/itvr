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
    redeemed = BooleanField(default=False)
    # sharepoint id. If something goes wrong with notification we can find
    # issued rebates with blank NCDA ids to try resending.
    ncda_id = IntegerField(blank=True, null=True, db_index=True)

    def __str__(self):
        return "DL: " + self.drivers_licence + ", $" + str(self.rebate_max_amount)

    class Meta:
        db_table = "go_electric_rebate"
