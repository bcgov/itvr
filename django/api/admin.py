from django.contrib import admin
from .models.go_electric_rebate_application import GoElectricRebateApplication
from django.contrib.admin.templatetags import admin_modify
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# admin.site.unregister(User)
admin.site.unregister(Group)
submit_row = admin_modify.submit_row


def submit_row_custom(context):
    ctx = submit_row(context)
    ctx['show_save_and_add_another'] = False
    ctx['show_save_and_continue'] = False
    return ctx


admin_modify.submit_row = submit_row_custom


@admin.register(GoElectricRebateApplication)
class GoElectricRebateApplicationAdmin(admin.ModelAdmin):
    readonly_fields = (
        "id",
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
        "doc1_tag",
        "doc2",
        "doc2_tag",
        "create_user",
        "update_user"
    )

    def has_delete_permission(self, request, obj=None):
        return False
