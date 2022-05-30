from unittest import TestCase
from rest_framework.serializers import ValidationError
from django.test import TestCase
from ...models.go_electric_rebate_application import GoElectricRebateApplication
from django.contrib.auth import get_user_model
from ..calculate_rebate import calculate_rebate_amount


class TestCalculate(TestCase):
    def setUp(self):
        super().setUp()

        user = get_user_model()
        user.objects.create(id=1, username="tester")

        GoElectricRebateApplication.objects.create(
            id="B5t92XeH7NnFUwxc",
            user_id=1,
            sin="302435839",
            application_type="individual",
            last_name="test",
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

    def test_application_a_ind(self):
        # qualifies for an individual rebate of a
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "65687"}
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, 4000)

    def test_application_b_ind(self):
        # qualifies for an individual rebate of b
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "85687"}
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, 2000)

    def test__application_c_ind(self):
        # qualifies for an individual rebate of 'c'
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "95687"}
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, 1000)

    def test__application_na_ind(self):
        # qualifies for an individual rebate of 'c'
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "105687"}
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "not approved")

    def test__application_a_ind_a_hs(self):
        # qualifies for a individual rebate of 'a' even though its a household application
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "75000"},
                {"sin": "270300379", "year": "2020", "income": "49000"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, 4000)

    def test_application_b_ind_c_hs(self):
        # qualifies for 'b' individual or 'c' household (gets b)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "85000"},
                {"sin": "270300379", "year": "2020", "income": "70000"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, 2000)

    def test_application_c_ind_b_hs(self):
        # qualifies for 'c' individual and 'b' household (should get b)
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "95000"},
                {"sin": "270300379", "year": "2020", "income": "50000"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, 2000)

    def test_application_na_ind_a_hs(self):
        # too high personal income but qualifies for 'a' household
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "100001"},
                {"sin": "270300379", "year": "2020", "income": "1"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, 4000)

    def test_application_na_ind_hs(self):
        # too high invididual AND household income
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "100002"},
                {"sin": "270300379", "year": "2020", "income": "100100"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "not approved")

    def test_application_no_cra(self):
        # too high invididual AND household income
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": None},
                {"sin": "270300379", "year": "2020", "income": "100100"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "not approved")
