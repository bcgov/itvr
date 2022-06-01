from ..models.go_electric_rebate_application import GoElectricRebateApplication
from ..models.household_member import HouseholdMember
from ..settings import INCOME_REBATES
from enum import Enum


class RebateType(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "Not Approved"


def get_cra_results(cra_response):
    filtered_applications = GoElectricRebateApplication.objects.select_related(
        "householdmember"
    ).filter(id__in=list(cra_response.keys()))
    # iterate through the entire cra response, call calculate function
    # for each seperate id
    rebates = {}
    for each in filtered_applications:
        single_cra_response = cra_response.get(each.id)
        rebate = calculate_rebate_amount(single_cra_response, each)
        rebates[each.id] = rebate
    return rebates


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
    if secondary_income is None:
        return check_individual(primary_income)
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


def calculate_rebate_amount(cra_response, filtered_applications):
    primary_applicant = next(
        (x for x in cra_response if x["sin"] == filtered_applications.sin), None
    )
    primary_income = primary_applicant.get("income")
    individual_rebate = check_individual(primary_income)
    if (
        individual_rebate == RebateType.A.value
        or len(cra_response) == 1
        or primary_income == None
    ):
        if individual_rebate == RebateType.D.value:
            return RebateType.D.value
        else:
            return INCOME_REBATES.get(individual_rebate).get("rebate")

    elif len(cra_response) > 1:
        hm = filtered_applications.householdmember
        secondary_applicant = next(
            (x for x in cra_response if x["sin"] == hm.sin), None
        )
        secondary_income = secondary_applicant.get("income")
        household_rebate = check_household(primary_income, secondary_income)
        return get_final_rebate(individual_rebate, household_rebate)
