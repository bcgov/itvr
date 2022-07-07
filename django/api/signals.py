from django.db.models.signals import post_save
from .models.go_electric_rebate_application import (
    GoElectricRebateApplication,
)
from .models.household_member import HouseholdMember
from .models.go_electric_rebate import GoElectricRebate
from django.dispatch import receiver
from django.conf import settings
from api.models.household_member import HouseholdMember
from django_q.tasks import async_task
from api.utility import addresses_match


@receiver(post_save, sender=GoElectricRebateApplication)
def create_application(sender, instance, created, **kwargs):
    if created and settings.EMAIL["SEND_EMAIL"]:
        async_task("api.tasks.send_individual_confirm", instance.email, instance.id)
        if instance.application_type == "household":
            async_task(
                "api.tasks.send_spouse_initial_message",
                instance.spouse_email,
                instance.id,
                instance.email,
            )


@receiver(post_save, sender=HouseholdMember)
def after_household_member_save(sender, instance, created, **kwargs):
    if created:
        application = instance.application
        primary_user = application.user
        secondary_user = instance.user
        if application.status != GoElectricRebateApplication.Status.CANCELLED:
            if (
                primary_user.identity_provider == "bcsc"
                and secondary_user.identity_provider == "bcsc"
                and addresses_match(application, secondary_user)
            ):
                application.status = GoElectricRebateApplication.Status.VERIFIED
                application.save()
            else:
                application.status = GoElectricRebateApplication.Status.SUBMITTED
                application.save()

            if settings.EMAIL["SEND_EMAIL"]:
                async_task(
                    "api.tasks.send_household_confirm",
                    application.email,
                    application.id,
                )


@receiver(post_save, sender=GoElectricRebateApplication)
def after_status_change(sender, instance, created, **kwargs):
    if (
        (not created)
        and (kwargs.get("update_fields") == {"status"})
        and (settings.EMAIL["SEND_EMAIL"])
    ):
        # if identity is declined (eg id doesnt match address)
        if instance.status == GoElectricRebateApplication.Status.DECLINED:
            async_task(
                "api.tasks.send_reject",
                instance.email,
                instance.id,
            )
        # if rebate is approved, send an email with amount
        elif instance.status == GoElectricRebateApplication.Status.APPROVED:
            rebate_amount = kwargs.get("rebate_amount")
            async_task(
                "api.tasks.send_approve", instance.email, instance.id, rebate_amount
            )
        # if application is not approved due to cra:
        elif instance.status == GoElectricRebateApplication.Status.NOT_APPROVED:
            async_task(
                "api.tasks.send_not_approve",
                instance.email,
                instance.id,
                instance.tax_year,
            )
        elif instance.status == GoElectricRebateApplication.Status.CANCELLED:
            async_task(
                "api.tasks.send_cancel",
                instance.email,
                instance.id,
            )


@receiver(post_save, sender=GoElectricRebate)
def after_rebate_issued(sender, instance, created, **kwargs):
    if created:
        async_task(
            "api.services.ncda.notify",
            instance.drivers_licence,
            instance.last_name,
            instance.expiry_date.strftime("%m/%d/%Y"),
            str(instance.rebate_max_amount),
            instance.id,
        )
