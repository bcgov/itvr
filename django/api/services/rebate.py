from api.models.go_electric_rebate_application import GoElectricRebateApplication
from api.models.go_electric_rebate import GoElectricRebate
from datetime import date, timedelta
from django.db.models.signals import post_save


# gets applications from rebates
def get_applications(rebates):
    ids = []
    if rebates is not None:
        ids = list(rebates)
    return GoElectricRebateApplication.objects.in_bulk(ids)


# saves approved rebates to the rebate table; returns the saved rebates
def save_rebates(rebates, applications):
    result = []
    if rebates is not None and applications is not None:
        rebate_objs = []
        for application_id, rebate_amount in rebates.items():
            if rebate_amount != "Not Approved":
                application = applications.get(application_id)
                if application is not None:
                    rebate_obj = GoElectricRebate(
                        application=application,
                        drivers_licence=application.drivers_licence,
                        last_name=application.last_name,
                        expiry_date=date.today() + timedelta(days=365),
                        rebate_max_amount=rebate_amount,
                        rebate_state=False,
                    )
                    rebate_objs.append(rebate_obj)
        result = GoElectricRebate.objects.bulk_create(rebate_objs)
    return result


# updates application statuses; emits signals manually
def update_application_statuses(rebates, applications):
    if rebates is not None and applications is not None:
        application_objs = []
        for application_id, rebate_amount in rebates.items():
            application = applications.get(application_id)
            if application is not None:
                if rebate_amount == "Not Approved":
                    application.status = GoElectricRebateApplication.Status.DECLINED
                else:
                    application.status = GoElectricRebateApplication.Status.APPROVED
                application_objs.append(application)
        GoElectricRebateApplication.objects.bulk_update(application_objs, ["status"])
        for application in application_objs:
            post_save.send(
                sender=GoElectricRebateApplication,
                instance=application,
                created=False,
                update_fields={"status"},
                rebate_amount=rebates.get(application.id),
            )
