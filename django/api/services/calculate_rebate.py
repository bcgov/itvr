from ..models.go_electric_rebate_application import GoElectricRebateApplication
from ..models.household_member import HouseholdMember
from ..settings import INCOME_REBATES
from enum import Enum


class RebateType(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "Not Approved"


def check_individual(primary_income):
    if primary_income is None:
        return RebateType.D.value
    primary_income = int(primary_income)
    if primary_income > INCOME_REBATES.get(RebateType.C.value).get("individual_income"):
        return RebateType.D.value
    elif primary_income <= INCOME_REBATES.get(RebateType.A.value).get(
        "individual_income"
    ):
        return RebateType.A.value
    elif primary_income <= INCOME_REBATES.get(RebateType.B.value).get(
        "individual_income"
    ):
        return RebateType.B.value
    elif primary_income <= INCOME_REBATES.get(RebateType.C.value).get(
        "individual_income"
    ):
        return RebateType.C.value


def check_household(primary_income, secondary_income):
    if (primary_income is None) | (secondary_income is None):
        return RebateType.D.value
    household_income = int(primary_income) + int(secondary_income)
    if household_income > INCOME_REBATES.get(RebateType.C.value).get(
        "household_income"
    ):
        return RebateType.D.value
    if household_income <= INCOME_REBATES.get(RebateType.A.value).get(
        "household_income"
    ):
        return RebateType.A.value
    elif household_income <= INCOME_REBATES.get(RebateType.B.value).get(
        "household_income"
    ):
        return RebateType.B.value
    elif household_income <= INCOME_REBATES.get(RebateType.C.value).get(
        "household_income"
    ):
        return RebateType.C.value


def get_final_rebate(individual_rebate, household_rebate):
    if household_rebate == RebateType.A.value:
        return INCOME_REBATES.get(RebateType.A.value).get("rebate")
    if (
        individual_rebate == RebateType.B.value
        or household_rebate == RebateType.B.value
    ):
        return INCOME_REBATES.get(RebateType.B.value).get("rebate")
    if (
        individual_rebate == RebateType.C.value
        or household_rebate == RebateType.C.value
    ):
        return INCOME_REBATES.get(RebateType.C.value).get("rebate")
    if (
        household_rebate == RebateType.D.value
        and individual_rebate == RebateType.D.value
    ):
        return RebateType.D.value


def calculate_rebate_amount(cra_response):
    application_id = list(cra_response.keys())[0]
    application = cra_response.get(application_id)
    filtered_applications = GoElectricRebateApplication.objects.select_related(
        "householdmember"
    ).get(id__in=[application_id])
    for idx, x in enumerate(application):
        # loop through the application lists provided by cra and check against
        # our database, find our record for that application id and
        # determine which item in the array is primary or secondary
        if x["sin"] == filtered_applications.sin:
            primary_applicant = application[idx]
    primary_income = primary_applicant.get("income")
    individual_rebate = check_individual(primary_income)
    if individual_rebate == RebateType.A.value or len(application) == 1:
        if individual_rebate == RebateType.D.value:
            return RebateType.D.value
        else:
            return INCOME_REBATES.get(individual_rebate).get("rebate")

    elif len(application) > 1:
        for idx, x in enumerate(application):
            if x["sin"] == filtered_applications.householdmember.sin:
                secondary_applicant = application[idx]
        secondary_income = secondary_applicant.get("income")
        household_rebate = check_household(primary_income, secondary_income)
        return get_final_rebate(individual_rebate, household_rebate)
