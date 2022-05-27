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

    def test_individual_application_a(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "65687"}
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "a")

    def test_individual_application_b(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "85687"}
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "b")

    def test_individual_application_c(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "95687"}
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "c")

    def test_household_application_a_ind(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "75000"},
                {"sin": "270300379", "year": "2020", "income": "49000"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "a")

    def test_household_application_b_ind(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "75000"},
                {"sin": "270300379", "year": "2020", "income": "60000"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        print(individual.id, cra_response)
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "b")

    def test_household_application_c_ind(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "75000"},
                {"sin": "270300379", "year": "2020", "income": "80000"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        print(individual.id, cra_response)
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "c")

    def test_application_a_hshld(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "100001"},
                {"sin": "270300379", "year": "2020", "income": "1"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        print(individual.id, cra_response)
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "a")

    def test_application_na_hshld(self):
        cra_response = {
            "B5t92XeH7NnFUwxc": [
                {"sin": "302435839", "year": "2020", "income": "100002"},
                {"sin": "270300379", "year": "2020", "income": "100100"},
            ],
        }
        individual = GoElectricRebateApplication.objects.get(id="B5t92XeH7NnFUwxc")
        print(individual.id, cra_response)
        rebate_amount = calculate_rebate_amount(cra_response, individual.id)
        self.assertEqual(rebate_amount, "a")
