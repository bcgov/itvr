import uuid
from django.conf import settings
from django.db.models import (
    CharField,
    IntegerField,
    ImageField,
    DateField,
    EmailField,
    BooleanField,
    UUIDField,
    PROTECT,
    ForeignKey,
    TextChoices,
)
from encrypted_fields.fields import EncryptedCharField
from django.utils.html import mark_safe
from django.core.files.storage import get_storage_class
from django.core.validators import MinLengthValidator
from api.validators import validate_driving_age, validate_sin, validate_consent
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

media_storage = get_storage_class()()


class GoElectricRebateApplication(TimeStampedModel):
    class Status(TextChoices):
        HOUSEHOLD_INITIATED = ("household_initiated", _("Household Initiated"))
        SUBMITTED = ("submitted", _("Submitted"))
        VERIFIED = ("verified", _("Verified"))
        DECLINED = ("declined", _("Declined"))

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
    )
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sin = EncryptedCharField(max_length=9, unique=False, validators=[validate_sin])
    status = CharField(max_length=250, choices=Status.choices, unique=False)
    last_name = CharField(max_length=250, unique=False)
    first_name = CharField(max_length=250, unique=False)
    middle_names = CharField(max_length=250, unique=False, blank=True, null=True)
    email = EmailField(max_length=250, unique=False)
    address = CharField(max_length=250, unique=False)
    city = CharField(max_length=250, unique=False)
    postal_code = CharField(max_length=6, unique=False)
    drivers_licence = CharField(
        max_length=8, unique=False, validators=[MinLengthValidator(7)]
    )
    date_of_birth = DateField(validators=[validate_driving_age])
    tax_year = IntegerField()
    doc1 = ImageField(upload_to="docs")

    def doc1_tag(self):
        return mark_safe(
            '<img src="%s" width="800" />'
            % (media_storage.url(name=self.doc1.file.name))
        )

    doc1_tag.short_description = "First Uploaded Document"

    doc2 = ImageField(upload_to="docs")

    def doc2_tag(self):
        return mark_safe(
            '<img src="%s" width="800" />'
            % (media_storage.url(name=self.doc2.file.name))
        )

    doc2_tag.short_description = "Second Uploaded Document"

    verified = BooleanField()

    spouse_email = EmailField(max_length=250, unique=False, null=True, blank=True)

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
