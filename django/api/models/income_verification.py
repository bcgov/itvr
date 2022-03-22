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

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'income_verification'
