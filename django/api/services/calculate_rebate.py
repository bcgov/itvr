def calculate_rebate_amount(cra_response, application_id):
    def check_individual(primary_income):

        if primary_income is None:
            return ""
        primary_income = int(primary_income)
        if primary_income > 100000:
            return ""
        elif primary_income > 90000:
            return "c"
        elif primary_income > 80000:
            return "b"
        elif primary_income <= 80000:
            return "a"

    def check_household(primary_income, secondary_income):
        if (primary_income is None) | (secondary_income is None):
            return ""
        household_income = int(primary_income) + int(secondary_income)
        if household_income > 165000:
            return ""
        elif household_income > 145000:
            return "c"
        elif household_income > 125000:
            return "b"
        if household_income <= 125000:
            return "a"

    def get_final_rebate(individual_rebate, household_rebate):
        if household_rebate == "a":
            return household_rebate
        if individual_rebate == "b" or household_rebate == "b":
            return "b"
        if individual_rebate == "c" or household_rebate == "c":
            return "c"

    application = cra_response.get(application_id)
    primary_applicant = application[0]
    primary_income = primary_applicant.get("income")

    if len(application) > 1:
        secondary_applicant = application[1]
        secondary_income = secondary_applicant.get("income")
        household_rebate = check_household(primary_income, secondary_income)

        if household_rebate == "":
            return "not approved"
        else:
            return household_rebate
    else:
        individual_rebate = check_individual(primary_income)
        if individual_rebate == "":
            return "not approved"
        else:
            return individual_rebate
