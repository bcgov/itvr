from django.contrib import admin
from .models.income_verification import IncomeVerification

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
