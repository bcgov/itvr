import uuid
from django.db.models import CharField, IntegerField, ImageField, \
    DateField, EmailField, BooleanField, UUIDField
from encrypted_fields.fields import EncryptedCharField
from auditable.models import Auditable
from django.utils.html import mark_safe
from django.core.files.storage import get_storage_class

media_storage = get_storage_class()()


class GoElectricRebateApplication(Auditable):
    id = UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sin = EncryptedCharField(
        max_length=9,
        unique=False
    )
    last_name = CharField(
        max_length=250,
        unique=False
    )
    first_name = CharField(
        max_length=250,
        unique=False
    )
    middle_names = CharField(
        max_length=250,
        unique=False,
        blank=True,
        null=True
    )
    email = EmailField(
        max_length=250,
        unique=False
    )
    address = CharField(
        max_length=250,
        unique=False
    )
    city = CharField(
        max_length=250,
        unique=False
    )
    postal_code = CharField(
        max_length=6,
        unique=False
    )
    drivers_licence = CharField(
        max_length=10,
        unique=False
    )
    date_of_birth = DateField()
    tax_year = IntegerField()
    doc1 = ImageField(upload_to='docs')

    def doc1_tag(self):
        return mark_safe(
            '<img src="%s" width="800" />'
            % (media_storage.url(name=self.doc1.file.name))
        )

    doc1_tag.short_description = 'First Uploaded Document'

    doc2 = ImageField(upload_to='docs')

    def doc2_tag(self):
        return mark_safe(
            '<img src="%s" width="800" />'
            % (media_storage.url(name=self.doc2.file.name))
        )

    doc2_tag.short_description = 'Second Uploaded Document'

    verified = BooleanField()

    def __str__(self):
        return self.last_name + ', ' + self.first_name

    class Meta:
        db_table = 'go_electric_rebate_application'
