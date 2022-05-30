from ..models.go_electric_rebate_application import GoElectricRebateApplication
from ..models.household_member import HouseholdMember


def calculate_rebate_amount(cra_response, application_id):
    rebate_numbers = {"a": 4000, "b": 2000, "c": 1000, "not approved": "not approved"}

    def check_individual(primary_income):
        if primary_income is None:
            return "not approved"
        primary_income = int(primary_income)
        if primary_income > 100000:
            return "not approved"
        elif primary_income > 90000:
            return "c"
        elif primary_income > 80000:
            return "b"
        elif primary_income <= 80000:
            return "a"

    def check_household(primary_income, secondary_income):
        if (primary_income is None) | (secondary_income is None):
            return "not approved"
        household_income = int(primary_income) + int(secondary_income)
        if household_income > 165000:
            return "not approved"
        elif household_income > 145000:
            return "c"
        elif household_income > 125000:
            return "b"
        if household_income <= 125000:
            return "a"

    def get_final_rebate(individual_rebate, household_rebate):
        if household_rebate == "a":
            return rebate_numbers.get(household_rebate)
        if individual_rebate == "b" or household_rebate == "b":
            return rebate_numbers.get("b")
        if individual_rebate == "c" or household_rebate == "c":
            return rebate_numbers.get("c")
        if household_rebate == "not approved" and individual_rebate == "not approved":
            return "not approved"

    application = cra_response.get(application_id)
    primary_applicant = {}
    secondary_applicant = {}
    filtered_applications = GoElectricRebateApplication.objects.filter(
        id=application_id
    )
    filtered_household = HouseholdMember.objects.filter(application=application_id)
    for idx, x in enumerate(application):
        # loop through the application lists provided by cra and check against
        # our database, find our record for that application id and
        # determine which item in the array is primary or secondary
        if x["sin"] == filtered_applications[0].sin:
            primary_applicant = application[idx]
    primary_income = primary_applicant.get("income")
    individual_rebate = check_individual(primary_income)
    if individual_rebate == "a" or len(application) == 1:
        return rebate_numbers.get(individual_rebate)

    elif len(application) > 1:
        for idx, x in enumerate(application):
            if x["sin"] == filtered_household[0].sin:
                secondary_applicant = application[idx]
        secondary_income = secondary_applicant.get("income")
        household_rebate = check_household(primary_income, secondary_income)
        return get_final_rebate(individual_rebate, household_rebate)
