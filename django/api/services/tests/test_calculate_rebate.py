from api.services.tests.test_rebate import TestRebate
from ...models.go_electric_rebate_application import GoElectricRebateApplication
from ..calculate_rebate import (
    calculate_individual_rebate_amount,
    get_cra_results_individuals_only,
)
from ...constants import RebateType, INCOME_REBATES


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
            "ctW8gU57YX4xfQ9o": [
                {"sin": "302435839", "year": "2020", "income": "65687"}
            ],
        }

        filtered_applications = GoElectricRebateApplication.objects.filter(
            id__in=list(cra_response.keys())
        )
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_individual_rebate_amount(
                single_cra_response, each
            )
            self.assertEqual(
                rebate_amount, INCOME_REBATES.get(RebateType.A.value).get("rebate")
            )

    def test_individual_receives_rebate_b(self):
        # qualifies for an individual rebate of 'B' (income of 85687)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "85687"}
            ],
            "ctW8gU57YX4xfQ9o": [
                {"sin": "302435839", "year": "2020", "income": "85687"}
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.filter(
            id__in=list(cra_response.keys())
        )
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_individual_rebate_amount(
                single_cra_response, each
            )
            self.assertEqual(
                rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
            )

    def test_individual_receives_rebate_c(self):
        # qualifies for an individual rebate of 'C' (income of 95687)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "95687"}
            ],
            "ctW8gU57YX4xfQ9o": [
                {"sin": "302435839", "year": "2020", "income": "95687"}
            ],
        }
        filtered_applications = GoElectricRebateApplication.objects.filter(
            id__in=list(cra_response.keys())
        )
        for each in filtered_applications:
            single_cra_response = cra_response.get(each.id)
            rebate_amount = calculate_individual_rebate_amount(
                single_cra_response, each
            )
            self.assertEqual(
                rebate_amount, INCOME_REBATES.get(RebateType.C.value).get("rebate")
            )

    def test_individual_receives_not_approved_high_income(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "105687"}
            ],
        }
        application = GoElectricRebateApplication.objects.filter(
            id__in=list(cra_response.keys())
        ).first()
        single_cra_response = cra_response.get(application.id)
        rebate_amount = calculate_individual_rebate_amount(
            single_cra_response, application
        )
        self.assertEqual(rebate_amount, RebateType.D.value)

    def test_individual_receives_not_approved_no_cra_info(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [{"sin": "302435839", "year": "2020", "income": None}],
        }
        application = GoElectricRebateApplication.objects.filter(
            id__in=list(cra_response.keys())
        ).first()
        single_cra_response = cra_response.get(application.id)
        rebate_amount = calculate_individual_rebate_amount(
            single_cra_response, application
        )
        self.assertEqual(rebate_amount, RebateType.E.value)

    def test_individual_receives_not_approved_sin_mismatch(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "123456789", "year": "2020", "income": "65687"}
            ],
        }
        application = GoElectricRebateApplication.objects.filter(
            id__in=list(cra_response.keys())
        ).first()
        single_cra_response = cra_response.get(application.id)
        rebate_amount = calculate_individual_rebate_amount(
            single_cra_response, application
        )
        self.assertEqual(rebate_amount, RebateType.F.value)


    def test_iterate_cra(self):
        # checks cra results one by one
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "55687"}
            ],
            "9uXLvNQS5vkKnscD": [
                {"sin": "302435839", "year": "2020", "income": "85687"}
            ],
            "ctW8gU57YX4xfQ9o": [{"sin": "302435839", "year": "2020", "income": None}],
        }
        rebate_amounts = get_cra_results_individuals_only(cra_response)
        self.assertEqual(
            rebate_amounts.get("B5t92XeH7NnFUwxc"),
            INCOME_REBATES.get(RebateType.A.value).get("rebate"),
        )
        self.assertEqual(
            rebate_amounts.get("9uXLvNQS5vkKnscD"),
            INCOME_REBATES.get(RebateType.B.value).get("rebate"),
        )
        self.assertEqual(rebate_amounts.get("ctW8gU57YX4xfQ9o"), RebateType.E.value)
