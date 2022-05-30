from ..models.go_electric_rebate_application import GoElectricRebateApplication
from ..models.household_member import HouseholdMember
from ..settings import INCOME_REBATES


def calculate_rebate_amount(cra_response, application_id):
    def check_individual(primary_income):
        if primary_income is None:
            return "not approved"
        primary_income = int(primary_income)
        if primary_income > INCOME_REBATES.get("C").get("individual_income"):
            return "not approved"
        elif primary_income <= INCOME_REBATES.get("A").get("individual_income"):
            return "A"
        elif primary_income <= INCOME_REBATES.get("B").get("individual_income"):
            return "B"
        elif primary_income <= INCOME_REBATES.get("C").get("individual_income"):
            return "C"

    def check_household(primary_income, secondary_income):
        if (primary_income is None) | (secondary_income is None):
            return "not approved"
        household_income = int(primary_income) + int(secondary_income)
        if household_income > INCOME_REBATES.get("C").get("household_income"):
            return "not approved"
        if household_income <= INCOME_REBATES.get("A").get("household_income"):
            return "A"
        elif household_income <= INCOME_REBATES.get("B").get("household_income"):
            return "B"
        elif household_income <= INCOME_REBATES.get("C").get("household_income"):
            return "C"

    def get_final_rebate(individual_rebate, household_rebate):
        if household_rebate == "A":
            return INCOME_REBATES.get("A").get("rebate")
        if individual_rebate == "B" or household_rebate == "B":
            return INCOME_REBATES.get("B").get("rebate")
        if individual_rebate == "C" or household_rebate == "C":
            return INCOME_REBATES.get("C").get("rebate")
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
    if individual_rebate == "A" or len(application) == 1:
        if individual_rebate == "not approved":
            return "not approved"
        else:
            return INCOME_REBATES.get(individual_rebate).get("rebate")

    elif len(application) > 1:
        for idx, x in enumerate(application):
            if x["sin"] == filtered_household[0].sin:
                secondary_applicant = application[idx]
        secondary_income = secondary_applicant.get("income")
        household_rebate = check_household(primary_income, secondary_income)
        return get_final_rebate(individual_rebate, household_rebate)
