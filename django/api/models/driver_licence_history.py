from django.db.models import (
    CharField,
    PROTECT,
    ForeignKey,
)

from django.core.validators import MinLengthValidator
from django_extensions.db.models import TimeStampedModel
from api.models.go_electric_rebate_application import GoElectricRebateApplication
from django.utils.functional import classproperty


class DriverLicenceHistory(TimeStampedModel):
    application = ForeignKey(GoElectricRebateApplication, on_delete=PROTECT)
    drivers_licence = CharField(max_length=8, validators=[MinLengthValidator(7)])

    def __str__(self):
        return self.application.id + " - " + self.drivers_licence

    class Meta:
        db_table = "driver_licence_history"

    @classproperty
    def admin_label(cls):
        return "Driver's Licences History"

    @classproperty
    def admin_hide_view_change_buttons(cls):
        return True
