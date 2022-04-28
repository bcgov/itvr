from datetime import date
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError


def validate_driving_age(dob):
    birthday = date(dob.year, dob.month, dob.day)
    today = date.today()
    difference_in_years = relativedelta(today, birthday).years
    if difference_in_years < 16:
        raise ValidationError(
            "You must be 16 years or older to request a rebate, please check \
the date of birth entered."
        )


def validate_sin(sin):
    """
    Let's use this fictitious SIN to demonstrate:130692544
    Always multiply the SIN Number by this number:121 212 121
    (Multiply the top number by the bottom number)

    130 692 544
    121 212 121
    -----------
    160 394 584

    If you get a 2 digit # add the digits together.
    Notice here that 6*2=12, add 1 and 2 together and get 3.
    Then add all of these digits together: 1+6+0+3+9+4+5+8+4=40
    If the SIN is valid this # will be evenly divisible by 10.
    This is a 'valid' SIN.
    """

    if len(sin) != 9:
        raise ValidationError("Please ensure your SIN is 9 characters long.")

    multiplication_number = "121212121"
    multiplied_sin = ""
    for i in range(0, 9):
        multiplied = int(sin[i]) * int(multiplication_number[i])
        if multiplied > 9:
            sum_of_digits = sum(int(digit) for digit in str(multiplied))
            multiplied_sin += str(sum_of_digits)
        else:
            multiplied_sin += str(multiplied)
    summed = sum(int(x) for x in multiplied_sin)
    if summed % 10 != 0:
        raise ValidationError("Please enter a valid SIN.")


def validate_consent(has_consented):
    if not has_consented:
        raise ValidationError(
            "You must confirm both consent check boxes to submit your application."
        )
