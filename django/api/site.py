from django.contrib.admin import AdminSite
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from sequences import get_next_value
from django.conf import settings
from django import forms
from .models.go_electric_rebate_application import GoElectricRebateApplication
from .services import cra


class UploadFileForm(forms.Form):
    cra_response_file = forms.FileField()


class ITVRAdminSite(AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "cra-download", self.admin_view(self.download_file), name="cra-download"
            ),
            path("cra-upload", self.admin_view(self.upload_file), name="cra-upload"),
        ]

        return custom_urls + urls

    # Create the filename for a CRA in file.
    # This needs to be named properly on the file before being encrypted.
    # '.p7m' is automatically added when the file is encrypted using Entrust.
    def get_cra_filename(self):
        cra_env = settings.CRA_ENVIRONMENT
        cra_sequence = get_next_value("cra_sequence")
        filename = (
            "TO.{cra_env}TO#@@00.R7005.IN.BCVR.{cra_env}{cra_sequence:05}".format(
                cra_env=cra_env, cra_sequence=cra_sequence
            )
        )
        return filename

    def upload_file(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["cra_response_file"]
                # print(file)
                file_contents = file.read()
                # print(file_contents)
                data = cra.read(file_contents)
                print(data)
                # return HttpResponseRedirect("/success/url/")
                return HttpResponse("OK")
        else:
            form = UploadFileForm()
        return render(request, "upload.html", {"form": form})

    def download_file(self, request):
        rebates = GoElectricRebateApplication.objects.filter(
            status=GoElectricRebateApplication.Status.VERIFIED
        )

        if rebates.count() == 0:
            response = HttpResponse("No income to check.")
            return response

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
        response = HttpResponse(cra.write(data), content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=" + filename
        return response

    # inline or attachment
