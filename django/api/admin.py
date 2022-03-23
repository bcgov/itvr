from django.contrib import admin
from .models.income_verification import IncomeVerification
from django.contrib.admin.templatetags import admin_modify
submit_row = admin_modify.submit_row


def submit_row_custom(context):
    ctx = submit_row(context)
    ctx['show_save_and_add_another'] = False
    ctx['show_save_and_continue'] = False
    return ctx


admin_modify.submit_row = submit_row_custom


@admin.register(IncomeVerification)
class IncomeVerificationAdmin(admin.ModelAdmin):
    readonly_fields = (
        "sin",
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
        "doc2",
        "create_user",
        "update_user"
    )

    def has_delete_permission(self, request, obj=None):
        return False
