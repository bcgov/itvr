from api.models.go_electric_rebate_application import GoElectricRebateApplication
from api.models.go_electric_rebate import GoElectricRebate
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.utils import timezone
from ..constants import RebateType


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
            if (
                rebate_amount != RebateType.D.value
                and rebate_amount != RebateType.E.value
                and rebate_amount != RebateType.F.value
            ):
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
    return created_rebates


# updates application statuses; emits signals manually
def update_application_statuses(rebates, applications):
    if rebates is not None and applications is not None:
        application_objs = []
        for application_id, rebate_amount in rebates.items():
            application = applications.get(application_id)
            if application is not None:
                if rebate_amount == RebateType.D.value:
                    application.status = GoElectricRebateApplication.Status.NOT_APPROVED_HIGH_INCOME
                    application.not_approved_on = timezone.now()
                    application.approved_on = None
                elif rebate_amount == RebateType.E.value:
                    application.status = GoElectricRebateApplication.Status.NOT_APPROVED_NO_CRA_INFO
                    application.not_approved_on = timezone.now()
                    application.approved_on = None
                elif rebate_amount == RebateType.F.value:
                    application.status = (
                        GoElectricRebateApplication.Status.NOT_APPROVED_SIN_MISMATCH
                    )
                    application.not_approved_on = timezone.now()
                    application.approved_on = None
                else:
                    application.status = GoElectricRebateApplication.Status.APPROVED
                    application.approved_on = timezone.now()
                    application.not_approved_on = None
                application.modified = timezone.now()
                application_objs.append(application)
        GoElectricRebateApplication.objects.bulk_update(
            application_objs, ["status", "modified", "approved_on", "not_approved_on"]
        )
        for application in application_objs:
            post_save.send(
                sender=GoElectricRebateApplication,
                instance=application,
                created=False,
                update_fields={"status"},
            )
