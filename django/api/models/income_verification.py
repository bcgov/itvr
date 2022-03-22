from email.policy import default
from django.db.models import CharField, IntegerField, FileField, DateField, EmailField
from encrypted_fields.fields import EncryptedCharField
from auditable.models import Auditable


class IncomeVerification(Auditable):
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
        default=None
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
    doc1 = FileField(upload_to='docs')
    doc2 = FileField(upload_to='docs')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'income_verification'
