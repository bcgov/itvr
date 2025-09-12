from django_extensions.db.models import TimeStampedModel
from django.db.models import (
    IntegerField,
)


class CraFileTracker(TimeStampedModel):
    sequence_number = IntegerField()

    class Meta:
        db_table = "cra_file_tracker"
