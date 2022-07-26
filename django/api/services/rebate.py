from api.models.go_electric_rebate_application import GoElectricRebateApplication
from api.models.go_electric_rebate import GoElectricRebate
from datetime import date, timedelta
from django.db.models.signals import post_save
from api.services.calculate_rebate import RebateType
from django.utils import timezone


# gets applications from rebates
def get_applications(rebates):
    result = {}
    ids = []
    if rebates is not None:
        ids = list(rebates)
        applications = GoElectricRebateApplication.objects.filter(id__in=ids).filter(
            status__exact=GoElectricRebateApplication.Status.VERIFIED
        )
        for application in applications:
            result[application.id] = application
    return result


# saves approved rebates to the rebate table; returns the saved rebates
def save_rebates(rebates, applications):
    created_rebates = []
    if rebates is not None and applications is not None:
        rebate_objs = []
        for application_id, rebate_amount in rebates.items():
            if rebate_amount != RebateType.D.value:
                application = applications.get(application_id)
                if application is not None:
                    rebate_obj = GoElectricRebate(
                        application=application,
                        drivers_licence=application.drivers_licence,
                        last_name=application.last_name,
                        expiry_date=date.today() + timedelta(days=365),
                        rebate_max_amount=rebate_amount,
                        redeemed=False,
                    )
                    rebate_objs.append(rebate_obj)
        created_rebates = GoElectricRebate.objects.bulk_create(rebate_objs)
        for rebate in created_rebates:
            post_save.send(
                sender=GoElectricRebate,
                instance=rebate,
                created=True,
            )
    return created_rebates


# updates application statuses; emits signals manually
def update_application_statuses(rebates, applications):
    if rebates is not None and applications is not None:
        application_objs = []
        for application_id, rebate_amount in rebates.items():
            application = applications.get(application_id)
            if application is not None:
                if rebate_amount == RebateType.D.value:
                    application.status = GoElectricRebateApplication.Status.NOT_APPROVED
                else:
                    application.status = GoElectricRebateApplication.Status.APPROVED
                application.modified = timezone.now()
                application_objs.append(application)
        GoElectricRebateApplication.objects.bulk_update(
            application_objs, ["status", "modified"]
        )
        for application in application_objs:
            post_save.send(
                sender=GoElectricRebateApplication,
                instance=application,
                created=False,
                update_fields={"status"},
                rebate_amount=rebates.get(application.id),
            )
