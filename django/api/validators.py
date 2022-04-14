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


def validate_sin(sin):
    if len(sin) != 9:
        raise ValidationError(
            "Please ensure your SIN is 9 characters long."
        )

    multiplication_number = '121212121'
    new_str = ''

    for i in range(0, 9):
        multiplied = int(sin[i]) * int(multiplication_number[i])
        if multiplied > 9:
            sum_of_digits = 0
            for digit in str(multiplied):
                sum_of_digits += int(digit)
            new_str += str(sum_of_digits)
        else:
            new_str += str(multiplied)
    summed = sum(int(x) for x in new_str)
    if summed % 10 != 0:
        raise ValidationError(
            "Please enter a valid SIN."
        )
