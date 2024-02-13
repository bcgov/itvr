from datetime import date
from django.contrib.admin import AdminSite
from django.contrib import messages
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .services.rebate import get_applications, save_rebates, update_application_statuses
from .services.calculate_rebate import get_cra_results_individuals_only
from sequences import get_next_value
from django.conf import settings
from django import forms
from .models.go_electric_rebate_application import GoElectricRebateApplication
from .services import cra
from django.db import transaction


class UploadFileForm(forms.Form):
    cra_response_file = forms.FileField(
        help_text="Please upload the decoded CRA OUT file."
    )


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
    def get_cra_filename(self, program_code="BCVR", cra_env="A", cra_sequence="00001"):
        filename = "TO.{cra_env}TO#@@00.R7005.IN.{program_code}.{cra_env}{cra_sequence:05}".format(
            cra_env=cra_env, cra_sequence=cra_sequence, program_code=program_code
        )
        return filename

    @transaction.atomic
    def upload_file(self, request):
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES["cra_response_file"]
                if settings.USE_CRYPTO_SERVICE and file.name.endswith(".p7m"):
                    content = cra.decrypt_file(file)
                else:
                    content = file.read()
                data = content.decode(encoding="utf-8", errors="replace")
                rebates = get_cra_results_individuals_only(data)
                associated_applications = get_applications(rebates)
                save_rebates(rebates, associated_applications)
                update_application_statuses(rebates, associated_applications)
                messages.add_message(
                    request, messages.SUCCESS, "CRA OUT file uploaded successfully"
                )
                return HttpResponseRedirect("/admin")
        else:
            form = UploadFileForm()
        return render(request, "upload.html", {"form": form})

    @transaction.atomic
    def download_file(self, request):
        rebates = GoElectricRebateApplication.objects.filter(
            status=GoElectricRebateApplication.Status.VERIFIED
        )

        if rebates.count() == 0:
            response = HttpResponse("No income to check.")
            return response

        data = []
        cra_env = settings.CRA_ENVIRONMENT
        cra_sequence = get_next_value("cra_sequence")
        program_code = "BCVR"

        for rebate in rebates:
            data.append(
                {
                    "sin": rebate.sin,
                    "years": [rebate.tax_year],
                    "given_name": rebate.first_name,
                    "family_name": rebate.last_name,
                    "birth_date": rebate.date_of_birth.strftime("%Y%m%d"),
                    "application_id": rebate.id,
                }
            )

            # TODO this should be some kind of enum like the status is.
            if rebate.application_type == "household":
                household_member = rebate.householdmember
                data.append(
                    {
                        "sin": household_member.sin,
                        "years": [rebate.tax_year],
                        "given_name": household_member.first_name,
                        "family_name": household_member.last_name,
                        "birth_date": household_member.date_of_birth.strftime("%Y%m%d"),
                        "application_id": rebate.id,
                    }
                )

        filename = self.get_cra_filename(program_code, cra_env, cra_sequence)
        today = date.today().strftime("%Y%m%d")
        content = cra.write(
            data,
            today=today,
            program_code=program_code,
            cra_env=cra_env,
            cra_sequence=f"{cra_sequence:05}",
        )

        if settings.USE_CRYPTO_SERVICE:
            filename = filename + ".p7m"
            encrypted_content = cra.encrypt(content)
            response = HttpResponse(
                encrypted_content, content_type="application/octet-stream"
            )
        else:
            response = HttpResponse(content, content_type="text/plain")

        response["Content-Disposition"] = "attachment; filename=" + filename
        return response

    def refine_app(self, app):
        models = app.get("models")
        if models is not None:
            for model in models:
                model_cls = model["model"]
                if hasattr(model_cls, "admin_label"):
                    model["admin_label"] = model_cls.admin_label
                else:
                    model["admin_label"] = model["name"]
                if hasattr(model_cls, "admin_hide_view_change_buttons"):
                    model["admin_hide_view_change_buttons"] = (
                        model_cls.admin_hide_view_change_buttons
                    )
                else:
                    model["admin_hide_view_change_buttons"] = False

    def _build_app_dict(self, request, label=None):
        app_dict = super()._build_app_dict(request, label)
        if label:
            self.refine_app(app_dict)
        else:
            for app in app_dict.values():
                self.refine_app(app)
        return app_dict
