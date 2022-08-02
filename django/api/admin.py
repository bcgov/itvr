from django.contrib import admin
from .models.go_electric_rebate_application import (
    GoElectricRebateApplication,
    SubmittedGoElectricRebateApplication,
    InitiatedGoElectricRebateApplication,
)
from .models.household_member import HouseholdMember
from .models.go_electric_rebate import GoElectricRebate
from django.contrib import messages
from . import messages_custom


class HouseholdApplicationInline(admin.StackedInline):
    model = HouseholdMember
    exclude = ("sin", "doc1", "doc2", "user")
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "date_of_birth",
        "bcsc_address",
        "bcsc_city",
        "bcsc_postal_code",
        "doc1_tag",
        "doc2_tag",
        "consent_personal",
        "consent_tax",
    )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GoElectricRebateApplication)
class GoElectricRebateApplicationAdmin(admin.ModelAdmin):
    search_fields = ["drivers_licence", "id", "status"]
    exclude = ("sin",)
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "email",
        "user_is_bcsc",
        "address",
        "city",
        "postal_code",
        "drivers_licence",
        "date_of_birth",
        "tax_year",
        "doc1",
        "doc2",
        "application_type",
        "doc1_tag",
        "doc2_tag",
        "consent_personal",
        "consent_tax",
        "is_legacy",
    )


# The proxy model is used to avoid a Django limitation where a model can only
# be registered once on the admin panel. This locked down version will be used
# by government staff to verify or decline submitted applications
# by BCeID users.
@admin.register(SubmittedGoElectricRebateApplication)
class SubmittedGoElectricRebateApplicationAdmin(admin.ModelAdmin):
    search_fields = ["drivers_licence", "id", "status"]
    # disable bulk actions
    actions = None
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
        "user_is_bcsc",
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
        "is_legacy",
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

    def response_change(self, request, obj):
        ret = super().response_change(request, obj)
        if "approve_application" in request.POST:
            obj.status = GoElectricRebateApplication.Status.VERIFIED
            obj.save(update_fields=["status"])
        if "reject_application" in request.POST:
            obj.status = GoElectricRebateApplication.Status.DECLINED
            obj.save(update_fields=["status"])
        return ret

    def message_user(
        self,
        request,
        message,
        level=messages.INFO,
        extra_tags="",
        fail_silently=False,
    ):
        revised_level = level
        if "reject_application" in request.POST:
            revised_level = messages_custom.NEGATIVE_SUCCESS
        super().message_user(request, message, revised_level, extra_tags, fail_silently)


@admin.register(GoElectricRebate)
class GoElectricRebateAdmin(admin.ModelAdmin):
    pass


@admin.register(InitiatedGoElectricRebateApplication)
class InitiatedGoElectricRebateApplicationAdmin(admin.ModelAdmin):
    search_fields = ["drivers_licence", "id", "status"]
    # disable bulk actions
    actions = None
    exclude = (
        "sin",
        "doc1",
        "doc2",
        "user",
        "spouse_email",
        "status",
        "address",
        "city",
        "postal_code",
        "application_type",
        "doc1_tag",
        "doc2_tag",
        "consent_personal",
        "consent_tax",
    )
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "email",
        "user_is_bcsc",
        "drivers_licence",
        "date_of_birth",
        "tax_year",
        "is_legacy",
    )

    def get_queryset(self, request):
        return GoElectricRebateApplication.objects.filter(
            status=GoElectricRebateApplication.Status.HOUSEHOLD_INITIATED
        )

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        ret = super().response_change(request, obj)
        if "cancel_application" in request.POST:
            obj.status = GoElectricRebateApplication.Status.CANCELLED
            obj.save(update_fields=["status"])
        return ret

    def message_user(
        self,
        request,
        message,
        level=messages.INFO,
        extra_tags="",
        fail_silently=False,
    ):
        revised_level = level
        if "cancel_application" in request.POST:
            revised_level = messages_custom.NEGATIVE_SUCCESS
        super().message_user(request, message, revised_level, extra_tags, fail_silently)
