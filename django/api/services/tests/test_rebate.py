from django.test import TestCase
from ...models.go_electric_rebate_application import GoElectricRebateApplication
from ...models.household_member import HouseholdMember
from django.contrib.auth import get_user_model

User = get_user_model()


class TestRebate(TestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        User.objects.create(id=1, username="tester")
        User.objects.create(id=2, username="tester2")

        GoElectricRebateApplication.objects.create(
            id="B5t92XeH7NnFUwxc",
            user_id=1,
            sin="302435839",
            application_type="individual",
            last_name="1",
            first_name="person",
            doc1="image1.png",
            doc2="image2.png",
            consent_personal=True,
            consent_tax=True,
            date_of_birth="2000-01-01",
            email="test1@gov.bc.ca",
            address="3 street",
            city="Victoria",
            postal_code="v8s4j9",
            tax_year=2020,
            drivers_licence="1234567",
        )
        GoElectricRebateApplication.objects.create(
            id="9uXLvNQS5vkKnscD",
            user_id=1,
            sin="302435839",
            application_type="individual",
            last_name="2",
            first_name="person",
            doc1="image3.png",
            doc2="image4.png",
            consent_personal=True,
            consent_tax=True,
            date_of_birth="2000-01-01",
            email="test2@gov.bc.ca",
            address="2 street",
            city="Victoria",
            postal_code="v8s4j9",
            tax_year=2020,
            drivers_licence="1234568",
        )
        GoElectricRebateApplication.objects.create(
            id="ctW8gU57YX4xfQ9o",
            user_id=1,
            sin="302435839",
            application_type="individual",
            last_name="3",
            first_name="person",
            doc1="image5.png",
            doc2="image6.png",
            consent_personal=True,
            consent_tax=True,
            date_of_birth="2000-01-01",
            email="test3@gov.bc.ca",
            address="3 street",
            city="Victoria",
            postal_code="v8s4j9",
            tax_year=2020,
            drivers_licence="1234569",
        )
        HouseholdMember.objects.create(
            application_id="9uXLvNQS5vkKnscD",
            user_id=2,
            sin="270300379",
            last_name="4",
            first_name="test",
            doc1="image7.png",
            doc2="image8.png",
            consent_personal=True,
            consent_tax=True,
            date_of_birth="2000-01-01",
        )
