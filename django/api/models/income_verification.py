from django.db.models import CharField, IntegerField, FileField, DateField
from auditable.models import Auditable


class IncomeVerification(Auditable):
    sin = CharField(
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
    date_of_birth = DateField()
    tax_year = IntegerField()

    doc1 = FileField(upload_to='docs')
    doc2 = FileField(upload_to='docs')

    class Meta:
        db_table = 'income_verification'
