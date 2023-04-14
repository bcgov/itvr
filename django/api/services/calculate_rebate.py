from ..models.go_electric_rebate_application import GoElectricRebateApplication
from ..constants import RebateType, INCOME_REBATES


def get_cra_results_individuals_only(cra_response):
    applications = GoElectricRebateApplication.objects.filter(
        id__in=list(cra_response.keys())
    )
    rebates = {}
    for application in applications:
        single_cra_response = cra_response.get(application.id)
        rebate = calculate_individual_rebate_amount(single_cra_response, application)
        if rebate is not None:
            rebates[application.id] = rebate
    return rebates


def check_individual(primary_income):
    if primary_income is None:
        return RebateType.E.value
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


def calculate_individual_rebate_amount(cra_response, application):
    if len(cra_response) == 1:
        cra_info = cra_response[0]
        cra_sin = cra_info["sin"]
        application_sin = application.sin
        if cra_sin == application_sin or str(application_sin).startswith("9"):
            income = cra_info["income"]
            rebate_type = check_individual(income)
            if rebate_type == RebateType.E.value or rebate_type == RebateType.D.value:
                return rebate_type
            return INCOME_REBATES.get(rebate_type).get("rebate")
        else:
            return RebateType.F.value
    return None
