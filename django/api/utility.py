def format_postal_code(postal_code):
    if postal_code is not None:
        return postal_code.replace(" ", "")
    return None


def addresses_match(application, household_user):
    application_street_address = application.address
    household_street_address = household_user.street_address
    application_city = application.city
    household_city = household_user.locality
    application_postal_code = application.postal_code
    household_postal_code = household_user.postal_code

    if (not application_street_address) or (not household_street_address):
        return False

    if (not application_city) or (not household_city):
        return False

    if application_street_address != household_street_address:
        return False

    if application_city != household_city:
        return False

    if application_postal_code and (not household_postal_code):
        return False

    if (not application_postal_code) and household_postal_code:
        return False

    if application_postal_code != household_user.postal_code:
        return False

    return True


def get_applicant_full_name(application):
    if application.middle_names:
        return (
            application.first_name
            + " "
            + application.middle_names
            + " "
            + application.last_name
        )
    return application.first_name + " " + application.last_name
