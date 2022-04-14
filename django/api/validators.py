from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError


def validate_driving_age(dob):
    birthday = date(dob.year, dob.month, dob.day)
    today = date.today()
    difference_in_years = relativedelta(today, birthday).years
    if difference_in_years < 16:
        raise ValidationError(
            "You must be 16 years or older to request a rebate, please check the date of birth entered."
        )
