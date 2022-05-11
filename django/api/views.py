from django.http import HttpResponse
from django.db import transaction
from sequences import get_next_value
from django.conf import settings


def get_filename():
    cra_env = settings.CRA_ENVIRONMENT
    cra_sequence = get_next_value("cra_sequence")
    filename = "TO.{cra_env}TO#@@00.R7005.IN.BCVR.{cra_env}{cra_sequence:05}".format(
        cra_env=cra_env, cra_sequence=cra_sequence
    )
    return filename


def download_file(request, *args, **kwargs):
    # todo figure out these imports
    from .models.go_electric_rebate_application import GoElectricRebateApplication
    from .services.cra import write

    rebates = GoElectricRebateApplication.objects.filter(
        status=GoElectricRebateApplication.Status.VERIFIED
    )

    data = []

    for rebate in rebates:
        data.append(
            {
                "sin": rebate.sin,
                "year": str(rebate.tax_year),  # should we just save as string?
                "given_name": rebate.first_name,
                "family_name": rebate.last_name,
                "birth_date": rebate.date_of_birth.strftime("%Y-%m-%d"),
            }
        )

    print(data)
    print(write(data))

    filename = get_filename()
    print(filename)

    response = HttpResponse("Hello", content_type="text/plain")
    response["Content-Disposition"] = "inline; filename=" + filename
    return response


# inline or attachment
