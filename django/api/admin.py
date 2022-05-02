from django.contrib import admin
from .models.go_electric_rebate_application import GoElectricRebateApplication
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
    exclude = ("sin",)
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "email",
        "address",
        "city",
        "postal_code",
        "date_of_birth",
        "doc1",
        "doc1_tag",
        "doc2",
        "doc2_tag",
        "user",
        "consent_personal",
        "consent_tax",
    )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GoElectricRebateApplication)
class GoElectricRebateApplicationAdmin(admin.ModelAdmin):
    inlines = [HouseholdApplicationInline]
    exclude = ("sin",)
    readonly_fields = (
        "id",
        "application_type",
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
        "doc1",
        "doc1_tag",
        "doc2",
        "doc2_tag",
        "user",
        "spouse_email",
        "consent_personal",
        "consent_tax",
    )

    def has_delete_permission(self, request, obj=None):
        return False
