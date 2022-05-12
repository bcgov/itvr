from django.db.models.signals import post_save
from .models.go_electric_rebate_application import GoElectricRebateApplication
from .models.household_member import HouseholdMember
from django.dispatch import receiver
from django.conf import settings
from api.models.household_member import HouseholdMember
from django_q.tasks import async_task


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
    if not created:
        ## if identity is declined (eg id doesnt match address)
        if instance.status == GoElectricRebateApplication.Status.DECLINED:
            if settings.EMAIL["SEND_EMAIL"]:
                async_task(
                    "api.tasks.send_reject",
                    instance.email,
                    instance.id,
                )
        ## if rebate is approved, send an email with amount which we will need to pass in
        elif instance.status == GoElectricRebateApplication.Status.APPROVED:
            if settings.EMAIL["SEND_EMAIL"]:
                async_task(
                    "api.tasks.send_approve",
                    instance.email,
                    instance.id,
                )
