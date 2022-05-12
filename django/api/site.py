from django.contrib.admin import AdminSite
from django.http import HttpResponse
from sequences import get_next_value
from django.conf import settings
from .models.go_electric_rebate_application import GoElectricRebateApplication
from .services.cra import write


class ITVRAdminSite(AdminSite):
    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        urls = [path("cra-download", self.admin_view(self.download_file))] + urls

        return urls

    # Create the filename for a CRA in file.
    def get_cra_filename(self):
        cra_env = settings.CRA_ENVIRONMENT
        cra_sequence = get_next_value("cra_sequence")
        filename = (
            "TO.{cra_env}TO#@@00.R7005.IN.BCVR.{cra_env}{cra_sequence:05}".format(
                cra_env=cra_env, cra_sequence=cra_sequence
            )
        )
        return filename

    def download_file(self, request):
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

        filename = self.get_cra_filename()
        response = HttpResponse(write(data), content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=" + filename
        return response

    # inline or attachment
