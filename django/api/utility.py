def format_postal_code(postal_code):
    if postal_code is not None:
        return postal_code.replace(" ", "")
    return None


def addresses_match(application, household_user):
    result = True
    application_street_address = application.address
    application_city = application.city
    application_postal_code = application.postal_code

    if application_street_address != household_user.street_address:
        return False

    if application_city != household_user.locality:
        return False

    if application_postal_code is not None and household_user.postal_code is None:
        return False

    if application_postal_code is None and household_user.postal_code is not None:
        return False

    if application_postal_code != household_user.postal_code:
        return False

    return result
