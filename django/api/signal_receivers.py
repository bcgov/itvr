from django.db.models.signals import post_save
from .models.go_electric_rebate_application import (
    GoElectricRebateApplication,
)
from .models.household_member import HouseholdMember
from django.dispatch import receiver
from django.conf import settings
from api.models.household_member import HouseholdMember
from django_q.tasks import async_task
from api.utility import addresses_match
from .signals import household_application_saved


@receiver(post_save, sender=GoElectricRebateApplication)
def create_application(sender, instance, created, **kwargs):
    if created and settings.EMAIL["SEND_EMAIL"]:
        async_task("api.tasks.send_individual_confirm", instance.email, instance.id)


@receiver(household_application_saved, sender=GoElectricRebateApplication)
def after_household_application_created(sender, instance, created, **kwargs):
    if settings.EMAIL["SEND_EMAIL"]:
        spouse_email = kwargs.get("spouse_email")
        async_task(
            "api.tasks.send_spouse_initial_message",
            spouse_email,
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
