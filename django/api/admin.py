from django.contrib import admin
from .models.go_electric_rebate_application import (
    GoElectricRebateApplication,
    SubmittedGoElectricRebateApplication,
)
from .models.household_member import HouseholdMember
from django.contrib.admin.templatetags import admin_modify
from django.contrib.auth.models import Group

admin.site.unregister(Group)
submit_row = admin_modify.submit_row


def submit_row_custom(context):
    ctx = submit_row(context)
    ctx["show_save_and_add_another"] = False
    ctx["show_save_and_continue"] = False
    return ctx


admin_modify.submit_row = submit_row_custom


class HouseholdApplicationInline(admin.StackedInline):
    model = HouseholdMember
    exclude = ("sin", "doc1", "doc2", "user")
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "date_of_birth",
        "doc1_tag",
        "doc2_tag",
        "consent_personal",
        "consent_tax",
    )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SubmittedGoElectricRebateApplication)
class SubmittedGoElectricRebateApplicationAdmin(admin.ModelAdmin):
    exclude = (
        "sin",
        "doc1",
        "doc2",
        "user",
        "spouse_email",
        "status",
        "application_type",
    )
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "email",
        "address",
        "city",
        "postal_code",
        "drivers_licence",
        "date_of_birth",
        "tax_year",
        "doc1_tag",
        "doc2_tag",
        "consent_personal",
        "consent_tax",
    )

    def get_queryset(self, request):
        return GoElectricRebateApplication.objects.filter(
            status=GoElectricRebateApplication.Status.SUBMITTED
        )

    def get_inlines(self, request, obj=None):
        # TODO update this to use the proper enum later.
        if obj and obj.application_type == "household":
            return [HouseholdApplicationInline]
        else:
            return []

    def has_delete_permission(self, request, obj=None):
        return False
