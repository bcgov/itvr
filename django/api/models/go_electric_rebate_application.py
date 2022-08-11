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
    Q,
    UniqueConstraint,
    CheckConstraint,
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
    validate_file_safe,
)
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from django.utils.functional import classproperty
from api.signals import household_application_saved

media_storage = get_storage_class()()


class ApplicationManager(Manager):
    def create(self, **kwargs):
        spouse_email = kwargs.pop("spouse_email", None)
        obj = super().create(**kwargs)
        if spouse_email:
            household_application_saved.send(
                sender=GoElectricRebateApplication,
                instance=obj,
                created=True,
                spouse_email=spouse_email,
            )
        return obj


class GoElectricRebateApplication(TimeStampedModel):
    objects = ApplicationManager()

    class Status(TextChoices):
        HOUSEHOLD_INITIATED = ("household_initiated", _("Household Initiated"))
        SUBMITTED = ("submitted", _("Submitted"))
        VERIFIED = ("verified", _("Verified"))
        DECLINED = ("declined", _("Declined"))
        APPROVED = ("approved", _("Approved"))
        NOT_APPROVED = ("not_approved", _("Not Approved"))
        REDEEMED = ("redeemed", _("Redeemed"))
        EXPIRED = ("expired", _("Expired"))
        CANCELLED = ("cancelled", _("Cancelled"))

    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT, null=True)
    id = ShortUUIDField(length=16, primary_key=True, editable=False)
    is_legacy = BooleanField(editable=False, default=False)
    sin = EncryptedCharField(
        max_length=9, unique=False, validators=[validate_sin], null=True
    )
    status = CharField(max_length=250, choices=Status.choices, unique=False)
    last_name = CharField(max_length=250, unique=False, null=True)
    first_name = CharField(max_length=250, unique=False, null=True)
    middle_names = CharField(max_length=250, unique=False, blank=True, null=True)
    email = EmailField(max_length=250, unique=False, null=True)
    address = CharField(max_length=250, unique=False, null=True)
    city = CharField(max_length=250, unique=False, null=True)
    postal_code = CharField(max_length=6, unique=False, blank=True, null=True)
    drivers_licence = CharField(
        max_length=8, unique=False, validators=[MinLengthValidator(7)]
    )
    date_of_birth = DateField(validators=[validate_driving_age], null=True)
    tax_year = IntegerField(null=True)
    doc1 = ImageField(
        upload_to="docs",
        blank=True,
        null=True,
        validators=[validate_file_size, validate_file_safe],
    )

    def doc1_tag(self):
        return mark_safe(
            '<img src="%s" width="600" />'
            % (media_storage.url(name=self.doc1.file.name))
        )

    doc1_tag.short_description = "First Uploaded Document"

    doc2 = ImageField(
        upload_to="docs",
        blank=True,
        null=True,
        validators=[validate_file_size, validate_file_safe],
    )

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
        null=True,
    )
    consent_personal = BooleanField(validators=[validate_consent], null=True)
    consent_tax = BooleanField(validators=[validate_consent], null=True)

    def user_is_bcsc(self):
        if self.user.identity_provider == "bcsc":
            return True
        return False

    user_is_bcsc.short_description = "Address is BCSC Verified"

    def __str__(self):
        if self.is_legacy:
            return "preITVR " + str(self.id)
        else:
            return (
                self.last_name
                + ", "
                + self.first_name
                + ": "
                + str(self.id)
                + ": "
                + self.status
            )

    class Meta:
        db_table = "go_electric_rebate_application"
        constraints = [
            UniqueConstraint(
                fields=["drivers_licence"],
                condition=Q(
                    status__in=[
                        "household_initiated",
                        "submitted",
                        "approved",
                        "redeemed",
                        "verified",
                    ]
                ),
                name="verify_rebate_status",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(user__isnull=False),
                name="user_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(sin__isnull=False),
                name="sin_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(last_name__isnull=False),
                name="last_name_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(first_name__isnull=False),
                name="first_name_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(email__isnull=False),
                name="email_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(address__isnull=False),
                name="address_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(city__isnull=False),
                name="city_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(date_of_birth__isnull=False),
                name="date_of_birth_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(tax_year__isnull=False),
                name="tax_year_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(application_type__isnull=False),
                name="application_type_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(consent_personal__isnull=False),
                name="consent_personal_null_constraint",
            ),
            CheckConstraint(
                check=Q(is_legacy__exact=True) | Q(consent_tax__isnull=False),
                name="consent_tax_null_constraint",
            ),
        ]


# This is for the admin panel
class SubmittedGoElectricRebateApplication(GoElectricRebateApplication):
    class Meta:
        proxy = True

    @classproperty
    def admin_label(cls):
        return "Review Applications"

    @classproperty
    def admin_hide_view_change_buttons(cls):
        return True


class CancellableGoElectricRebateApplication(GoElectricRebateApplication):
    class Meta:
        proxy = True

    @classproperty
    def admin_label(cls):
        return "Cancel Applications"

    @classproperty
    def admin_hide_view_change_buttons(cls):
        return True


class SearchableGoElectricRebateApplication(GoElectricRebateApplication):
    class Meta:
        proxy = True
        ordering = ["-modified"]

    @classproperty
    def admin_label(cls):
        return "Search All Applications"

    @classproperty
    def admin_hide_view_change_buttons(cls):
        return True
