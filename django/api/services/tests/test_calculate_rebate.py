from unittest import TestCase
from django.test import TestCase
from ...models.go_electric_rebate_application import GoElectricRebateApplication
from ...models.household_member import HouseholdMember
from django.contrib.auth import get_user_model
from ..calculate_rebate import calculate_rebate_amount, RebateType
from ...settings import INCOME_REBATES


User = get_user_model()


class TestCalculate(TestCase):
    def setUp(self):
        User.objects.create(id=1, username="tester")
        User.objects.create(id=2, username="tester2")

        GoElectricRebateApplication.objects.create(
            id="B5t92XeH7NnFUwxc",
            user_id=1,
            sin="302435839",
            application_type="individual",
            last_name="person",
            first_name="person",
            doc1="image1.png",
            doc2="image2.png",
            consent_personal=True,
            consent_tax=True,
            date_of_birth="2000-01-01",
            email="emily.hillier@gov.bc.ca",
            address="123 street",
            city="Victoria",
            postal_code="v8s4j9",
            tax_year=2020,
        )
        HouseholdMember.objects.create(
            application_id="B5t92XeH7NnFUwxc",
            user_id=2,
            sin="270300379",
            last_name="test",
            first_name="test",
            doc1="image1.png",
            doc2="image2.png",
            consent_personal=True,
            consent_tax=True,
            date_of_birth="2000-01-01",
        )

    def test_individual_receives_rebate_a(self):
        # qualifies for an individual rebate of a
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "65687"}
            ],
        }

        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.A.value).get("rebate")
        )

    def test_individual_receives_rebate_b(self):
        # qualifies for an individual rebate of b
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "85687"}
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_individual_receives_rebate_c(self):
        # qualifies for an individual rebate of 'c'
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "95687"}
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.C.value).get("rebate")
        )

    def test_individual_receives_not_approved(self):
        # qualifies for an individual rebate of 'Not Approved'
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "105687"}
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)

        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.D.value).get("rebate")
        )

    def test_household_receives_rebate_a_individual(self):
        # qualifies for a individual rebate of 'a' even though its a household application
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "75000"},
                {"sin": "270300379", "year": "2020", "income": "49000"},
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.A.value).get("rebate")
        )

    def test_household_receives_rebate_b_individual(self):
        # qualifies for 'b' individual or 'c' household (gets b)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "85000"},
                {"sin": "270300379", "year": "2020", "income": "70000"},
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_household_receives_rebate_b(self):
        # qualifies for 'c' individual and 'b' household (should get b)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "95000"},
                {"sin": "270300379", "year": "2020", "income": "50000"},
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_household_receives_rebate_b_switched_cra(self):
        # qualifies for 'c' individual and 'b' household (should get b)
        # just switched cra response
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "270300379", "year": "2020", "income": "50000"},
                {"sin": "302435839", "year": "2020", "income": "95000"},
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.B.value).get("rebate")
        )

    def test_household_receives_rebate_a(self):
        # too high personal income but qualifies for 'a' household
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "100001"},
                {"sin": "270300379", "year": "2020", "income": "1"},
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.A.value).get("rebate")
        )

    def test_household_receives_not_approved(self):
        # too high invididual AND household income
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "100002"},
                {"sin": "270300379", "year": "2020", "income": "100100"},
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.D.value).get("rebate")
        )

    def test_application_no_cra(self):
        # no income
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": None},
                {"sin": "270300379", "year": "v", "income": "100100"},
            ],
        }
        rebate_amount = calculate_rebate_amount(cra_response)
        self.assertEqual(
            rebate_amount, INCOME_REBATES.get(RebateType.D.value).get("rebate")
        )
