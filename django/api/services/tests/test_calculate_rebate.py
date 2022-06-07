from api.services.tests.test_rebate import TestRebate
from ...models.go_electric_rebate_application import GoElectricRebateApplication
from ..calculate_rebate import calculate_rebate_amount, RebateType, get_cra_results
from ...settings import INCOME_REBATES


class TestCalculate(TestRebate):
    @classmethod
    def setUpClass(self):
        super().setUpClass()

    def test_individual_receives_rebate_a(self):
        # qualifies for an individual rebate of 'A' (income of 65687)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "65687"}
            ],
        }

        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.A.value).get("rebate")
        )

    def test_individual_receives_rebate_b(self):
        # qualifies for an individual rebate of 'B' (income of 85687)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "85687"}
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_individual_receives_rebate_c(self):
        # qualifies for an individual rebate of 'C' (income of 95687)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "95687"}
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.C.value).get("rebate")
        )

    def test_individual_receives_not_approved(self):
        # qualifies for an individual rebate of 'Not Approved' (income 105687)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "105687"}
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)

        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.D.value).get("rebate")
        )

    def test_household_receives_rebate_a_individual(self):
        # qualifies for a individual rebate of 'A' even though its a household application (primary income 75000, spouse 49000)
        cra_response = {
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": "75000"},
                {"sin": "270300379", "year": "2020", "income": "49000"},
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.A.value).get("rebate")
        )

    def test_household_receives_rebate_b_individual(self):
        # qualifies for 'B' individual or 'C' household (gets 'B') (primary income 85000, houehold 70000)
        cra_response = {
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": "85000"},
                {"sin": "270300379", "year": "2020", "income": "70000"},
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_household_receives_rebate_b(self):
        # qualifies for 'C' individual and 'B' household (should get 'B') (primary 95000, spouse 50000)
        cra_response = {
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": "95000"},
                {"sin": "270300379", "year": "2020", "income": "50000"},
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_household_receives_rebate_b_switched_cra(self):
        # qualifies for 'C' individual and 'B' household (should get 'B')
        # just switched cra response order (primary 95000, spouse 50000)
        cra_response = {
            "9uXLvNQS5vkKnscD": [
                {"sin": "270300379", "year": "2020", "income": "50000"},
                {"sin": "302435839", "year": "2020", "income": "95000"},
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)

        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_household_receives_rebate_a(self):
        # too high personal income but qualifies for 'A' household
        # (primary 10001, spouse 1)
        cra_response = {
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": "100001"},
                {"sin": "270300379", "year": "2020", "income": "1"},
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.A.value).get("rebate")
        )

    def test_household_receives_rebate_b_spouse_is_0(self):
        # too high personal income but qualifies for 'A' household
        # (primary 125001, spouse 0)
        cra_response = {
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": "125001"},
                {"sin": "270300379", "year": "2020", "income": "0"},
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_household_receives_not_approved(self):
        # too high invididual AND household income
        # (primary 100002, spouse 100100)
        cra_response = {
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": "100002"},
                {"sin": "270300379", "year": "2020", "income": "100100"},
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.D.value).get("rebate")
        )

    def test_household_no_primary_income_receives_rebate_d(self):
        # no income for primary, but income for spouse (should get 'D)
        cra_response = {
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": None},
                {"sin": "270300379", "year": "2020", "income": "100100"},
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.D.value).get("rebate")
        )

    def test_household_no_secondary_income_receives_individual_b(self):
        # no income for secondary so receives the primary amount 'B'
        # (primary 81000, spouse none)
        cra_response = {
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": 81000},
                {"sin": "270300379", "year": "2020", "income": None},
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.select_related(
            "householdmember"
        ).filter(id__in=list(cra_response.keys()))
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_rebate_amount(single_cra_response, each)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_iterate_cra(self):
        # checks cra results one by one
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "55687"}
            ],
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": "85687"},
                {"sin": "270300379", "year": "2020", "income": "81830"},
            ],
            "ctW8gU57YX4xfQ9o": [{"sin": "302435839", "year": "2020", "income": None}],
        }
        rebate_amounts = get_cra_results(cra_response)
        self.assertEqual(
            rebate_amounts.get("B5t92XeH7NnFUwxc"),
            INCOME_REBATES.get(RebateType.A.value).get("rebate"),
        )
        self.assertEqual(
            rebate_amounts.get("9uXLvNQS5vkKnscD"),
            INCOME_REBATES.get(RebateType.B.value).get("rebate"),
        )
        self.assertEqual(
            rebate_amounts.get("ctW8gU57YX4xfQ9o"),
            INCOME_REBATES.get(RebateType.D.value).get("rebate"),
        )
