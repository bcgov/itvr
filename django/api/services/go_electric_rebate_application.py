from api.models.go_electric_rebate_application import GoElectricRebateApplication
from django.db.models import Q


def equivalent_drivers_licence_number_found(
    drivers_licence_number, application_id=None
):
    equivalent_dl = drivers_licence_number
    if len(drivers_licence_number) == 7:
        equivalent_dl = "0" + drivers_licence_number
    elif len(drivers_licence_number) == 8 and drivers_licence_number.startswith("0"):
        equivalent_dl = drivers_licence_number[1:]
    exclude_lookup = {}
    if application_id is not None:
        exclude_lookup["id"] = application_id
    return (
        GoElectricRebateApplication.objects.filter(
            Q(drivers_licence__exact=drivers_licence_number)
            | Q(drivers_licence__exact=equivalent_dl)
        )
        .filter(
            status__in=[
                GoElectricRebateApplication.Status.SUBMITTED,
                GoElectricRebateApplication.Status.VERIFIED,
                GoElectricRebateApplication.Status.APPROVED,
                GoElectricRebateApplication.Status.REDEEMED,
            ]
        )
        .exclude(**exclude_lookup)
        .exists()
    )
