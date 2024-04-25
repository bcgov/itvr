def format_postal_code(postal_code):
    if postal_code is not None:
        return postal_code.replace(" ", "")
    return None


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
