from shortuuid.django_fields import ShortUUIDField
from django.conf import settings
from django.db.models import (
    CharField,
    IntegerField,
    ImageField,
    DateField,
    EmailField,
    BooleanField,
    PROTECT,
    ForeignKey,
    TextChoices,
    Manager,
)
from encrypted_fields.fields import EncryptedCharField
from django.utils.html import mark_safe
from django.core.files.storage import get_storage_class
from django.core.validators import MinLengthValidator
from api.validators import (
    validate_driving_age,
    validate_sin,
    validate_consent,
    validate_file_size,
)
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

media_storage = get_storage_class()()


class ApplicationManager(Manager):
    def create(self, **kwargs):
        spouse_email = kwargs.pop("spouse_email", None)
        obj = self.model(**kwargs)
        self._for_write = True
        if spouse_email:
            obj.spouse_email = spouse_email
        obj.save(force_insert=True, using=self.db)
        return obj


class GoElectricRebateApplication(TimeStampedModel):
    objects = ApplicationManager()

    class Status(TextChoices):
        HOUSEHOLD_INITIATED = ("household_initiated", _("Household Initiated"))
        SUBMITTED = ("submitted", _("Submitted"))
        VERIFIED = ("verified", _("Verified"))
        DECLINED = ("declined", _("Declined"))
        APPROVED = ("approved", _("Approved"))
        CRA_ERROR = ("cra_error", _("CRA Error"))
        REDEEMED = ("redeemed", _("Redeemed"))
        EXPIRED = ("expired", _("Expired"))

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
    )
    id = ShortUUIDField(length=16, primary_key=True, editable=False)
    sin = EncryptedCharField(max_length=9, unique=False, validators=[validate_sin])
    status = CharField(max_length=250, choices=Status.choices, unique=False)
    last_name = CharField(max_length=250, unique=False)
    first_name = CharField(max_length=250, unique=False)
    middle_names = CharField(max_length=250, unique=False, blank=True, null=True)
    email = EmailField(max_length=250, unique=False)
    address = CharField(max_length=250, unique=False)
    city = CharField(max_length=250, unique=False)
    postal_code = CharField(max_length=6, unique=False, blank=True, null=True)
    drivers_licence = CharField(
        max_length=8, unique=False, validators=[MinLengthValidator(7)]
    )
    date_of_birth = DateField(validators=[validate_driving_age])
    tax_year = IntegerField()
    doc1 = ImageField(upload_to="docs", validators=[validate_file_size])

    def doc1_tag(self):
        return mark_safe(
            '<img src="%s" width="600" />'
            % (media_storage.url(name=self.doc1.file.name))
        )

    doc1_tag.short_description = "First Uploaded Document"

    doc2 = ImageField(upload_to="docs", validators=[validate_file_size])

    def doc2_tag(self):
        return mark_safe(
            '<img src="%s" width="600" />'
            % (media_storage.url(name=self.doc2.file.name))
        )

    doc2_tag.short_description = "Second Uploaded Document"

    # TODO this should be some kind of enum like the status is.
    application_type = CharField(
        max_length=25,
        unique=False,
    )
    consent_personal = BooleanField(validators=[validate_consent])
    consent_tax = BooleanField(validators=[validate_consent])

    def __str__(self):
        return self.last_name + ", " + self.first_name + ": " + str(self.id)

    class Meta:
        db_table = "go_electric_rebate_application"


# This is for the admin panel
class SubmittedGoElectricRebateApplication(GoElectricRebateApplication):
    class Meta:
        proxy = True
