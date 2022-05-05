from django.conf import settings
from django.db.models import (
    CharField,
    ImageField,
    DateField,
    EmailField,
    BooleanField,
    PROTECT,
    ForeignKey,
    OneToOneField,
)
from encrypted_fields.fields import EncryptedCharField
from django.utils.html import mark_safe
from django.core.files.storage import get_storage_class
from django_extensions.db.models import TimeStampedModel
from api.validators import validate_driving_age, validate_sin, validate_consent

media_storage = get_storage_class()()


class HouseholdMember(TimeStampedModel):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=PROTECT,
    )
    application = OneToOneField(
        "GoElectricRebateApplication",
        on_delete=PROTECT,
    )
    sin = EncryptedCharField(max_length=9, unique=False, validators=[validate_sin])
    last_name = CharField(max_length=250, unique=False)
    first_name = CharField(max_length=250, unique=False)
    middle_names = CharField(max_length=250, unique=False, blank=True, null=True)
    email = EmailField(max_length=250, unique=False)
    date_of_birth = DateField(validators=[validate_driving_age])
    doc1 = ImageField(upload_to="docs")

    def doc1_tag(self):
        return mark_safe(
            '<img src="%s" width="600" />'
            % (media_storage.url(name=self.doc1.file.name))
        )

    doc1_tag.short_description = "First Uploaded Document"

    doc2 = ImageField(upload_to="docs")

    def doc2_tag(self):
        return mark_safe(
            '<img src="%s" width="600" />'
            % (media_storage.url(name=self.doc2.file.name))
        )

    doc2_tag.short_description = "Second Uploaded Document"

    consent_personal = BooleanField(validators=[validate_consent])
    consent_tax = BooleanField(validators=[validate_consent])

    def __str__(self):
        return self.last_name + ", " + self.first_name

    class Meta:
        db_table = "household_member"
