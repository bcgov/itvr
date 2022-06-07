from api.services.tests.test_rebate import TestRebate
from api.services.rebate import (
    get_applications,
    save_rebates,
    update_application_statuses,
)
from django.db.models.signals import post_save
from api.models.go_electric_rebate_application import GoElectricRebateApplication
from django.dispatch import receiver
from api.services.calculate_rebate import RebateType


class TestIssueRebate(TestRebate):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.rebates = {
            "9uXLvNQS5vkKnscD": 2000,
            "B5t92XeH7NnFUwxc": 4000,
            "ctW8gU57YX4xfQ9o": RebateType.D.value,
        }

        self.approved_rebates = {}
        for id, amount in self.rebates.items():
            if amount != RebateType.D.value:
                self.approved_rebates[id] = amount

        self.not_approved_rebates = set()
        for id, amount in self.rebates.items():
            if amount == RebateType.D.value:
                self.not_approved_rebates.add(id)

    def test_get_applications_from_rebates(self):
        # gets n applications if there are n rebates
        applications = get_applications(self.rebates)
        for application_id in self.rebates:
            self.assertIsNotNone(applications.get(application_id))

    def test_save_rebates(self):
        # saves m rebates (with the correct associated application information) if there are m approved rebates
        applications = get_applications(self.rebates)
        saved_rebates = save_rebates(self.rebates, applications)
        saved_rebates_dict = {}
        for rebate in saved_rebates:
            saved_rebates_dict[rebate.application_id] = rebate
        self.assertEqual(len(self.approved_rebates), len(saved_rebates))
        for application_id, amount in self.approved_rebates.items():
            self.assertIsNotNone(saved_rebates_dict.get(application_id))
            self.assertEqual(
                saved_rebates_dict[application_id].rebate_max_amount, amount
            )
            self.assertEqual(
                saved_rebates_dict[application_id].drivers_licence,
                applications[application_id].drivers_licence,
            )

    def test_update_application_statuses(self):
        # updates n applications correctly if there are n rebates; correct parameters sent to post_save signal listener
        declined_status = GoElectricRebateApplication.Status.DECLINED
        approved_status = GoElectricRebateApplication.Status.APPROVED
        declined_emails = set()
        rebate_emails = {}

        @receiver(post_save, sender=GoElectricRebateApplication)
        def listener(sender, instance, created, **kwargs):
            if (not created) and (kwargs.get("update_fields") == {"status"}):
                if instance.status == declined_status:
                    declined_emails.add(instance.id)
                elif instance.status == approved_status:
                    rebate_amount = kwargs.get("rebate_amount")
                    rebate_emails[instance.id] = rebate_amount

        applications = get_applications(self.rebates)
        update_application_statuses(self.rebates, applications)
        updated_applications = GoElectricRebateApplication.objects.filter(
            id__in=list(applications)
        ).filter(status__in=[declined_status, approved_status])

        self.assertEqual(len(updated_applications), len(applications))
        self.assertDictEqual(self.approved_rebates, rebate_emails)
        self.assertSetEqual(self.not_approved_rebates, declined_emails)
