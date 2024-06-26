from django.contrib import admin
from .models.go_electric_rebate_application import (
    GoElectricRebateApplication,
    GoElectricRebateApplicationWithFailedEmail,
    SearchableGoElectricRebateApplication,
    SubmittedGoElectricRebateApplication,
    CancellableGoElectricRebateApplication,
    DriverLicenceEditableGoElectricRebateApplication,
    ChangeRedeemedGoElectricRebateApplication,
    ExpiredGoElectricRebateApplication,
    LegacyGoElectricRebateApplication,
)
from .models.household_member import HouseholdMember
from .models.go_electric_rebate import GoElectricRebate
from .models.driver_licence_history import DriverLicenceHistory
from django.contrib import messages
from . import messages_custom
from django.db.models import Q
from django.db import transaction
from api.services.ncda import (
    delete_rebate,
    update_rebate,
    get_rebate_by_drivers_licence,
    notify,
)
from django_q.tasks import async_task
from api.services.go_electric_rebate_application import (
    equivalent_drivers_licence_number_found,
)
from api.model_forms.extend_expired_application import ExtendExpiryForm
from datetime import date, timedelta


class ITVRModelAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ITVRModelAdminStringent(ITVRModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False


class ITVRInlineAdmin(admin.StackedInline):
    actions = None

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class HouseholdApplicationInline(ITVRInlineAdmin):
    model = HouseholdMember
    extra = 0
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


def get_inlines(obj):
    # TODO update this to use the proper enum later.
    if obj and obj.application_type == "household":
        return [HouseholdApplicationInline]
    else:
        return []


@admin.register(GoElectricRebate)
class GoElectricRebateAdmin(ITVRModelAdminStringent):
    search_fields = ["application__id", "drivers_licence", "last_name", "ncda_id"]
    exclude = ("application",)
    readonly_fields = (
        "application_id",
        "drivers_licence",
        "last_name",
        "expiry_date",
        "rebate_max_amount",
        "redeemed",
        "ncda_id",
        "created",
        "modified",
    )


@admin.register(DriverLicenceHistory)
class DriverLicenceHistoryAdmin(ITVRModelAdminStringent):
    search_fields = ["application__id", "drivers_licence"]
    exclude = ("application",)
    readonly_fields = (
        "application_id",
        "drivers_licence",
        "created",
    )


@admin.register(GoElectricRebateApplication)
class GoElectricRebateApplicationAdmin(ITVRModelAdminStringent):
    exclude = ("sin", "user")


# The proxy model is used to avoid a Django limitation where a model can only
# be registered once on the admin panel. This locked down version will be used
# by government staff to verify or decline submitted applications
# by BCeID users.
@admin.register(SubmittedGoElectricRebateApplication)
class SubmittedGoElectricRebateApplicationAdmin(ITVRModelAdmin):
    search_fields = ["drivers_licence", "id", "status", "last_name"]
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
        "confirmation_email_success",
        "spouse_email_success",
        "created",
        "approved_on",
        "not_approved_on",
    )

    def get_queryset(self, request):
        return GoElectricRebateApplication.objects.filter(
            status=GoElectricRebateApplication.Status.SUBMITTED
        )

    def get_inlines(self, request, obj=None):
        return get_inlines(obj)

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


@admin.register(CancellableGoElectricRebateApplication)
class CancellableGoElectricRebateApplicationAdmin(ITVRModelAdmin):
    search_fields = ["drivers_licence", "id", "status", "last_name"]
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
        "reason_for_decline",
    )
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "status",
        "email",
        "user_is_bcsc",
        "drivers_licence",
        "date_of_birth",
        "tax_year",
        "is_legacy",
        "confirmation_email_success",
        "spouse_email_success",
        "created",
        "approved_on",
        "not_approved_on",
    )

    def get_queryset(self, request):
        return GoElectricRebateApplication.objects.filter(
            Q(status=GoElectricRebateApplication.Status.HOUSEHOLD_INITIATED)
            | Q(status=GoElectricRebateApplication.Status.SUBMITTED)
            | Q(status=GoElectricRebateApplication.Status.APPROVED)
            | Q(status=GoElectricRebateApplication.Status.VERIFIED)
        )

    def response_change(self, request, obj):
        ret = super().response_change(request, obj)
        if "cancel_application" in request.POST:
            dl = obj.drivers_licence
            obj.status = GoElectricRebateApplication.Status.CANCELLED
            obj.save(update_fields=["status"])
            rebate = GoElectricRebate.objects.filter(drivers_licence=dl).first()
            if rebate:
                ncda_id = rebate.ncda_id
                rebate.delete()
                if ncda_id is not None:
                    delete_rebate(ncda_id)
            try:
                async_task(
                    "api.tasks.send_cancel",
                    obj.email,
                    obj.id,
                )
            except Exception:
                pass

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


@admin.register(SearchableGoElectricRebateApplication)
class SearchableGoElectricRebateApplicationAdmin(ITVRModelAdminStringent):
    search_fields = ["drivers_licence", "id", "status", "last_name"]
    exclude = (
        "sin",
        "doc1",
        "doc2",
        "user",
    )
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "status",
        "email",
        "user_is_bcsc",
        "address",
        "city",
        "postal_code",
        "drivers_licence",
        "date_of_birth",
        "tax_year",
        "application_type",
        "doc1_tag",
        "doc2_tag",
        "consent_personal",
        "consent_tax",
        "is_legacy",
        "confirmation_email_success",
        "spouse_email_success",
        "reason_for_decline",
        "rebate_max_amount",
        "created",
        "approved_on",
        "not_approved_on",
    )

    def rebate_max_amount(self, obj):
        return (
            GoElectricRebate.objects.get(application_id=obj.id).rebate_max_amount
            if obj.status == "approved"
            else "-"
        )

    rebate_max_amount.short_description = "Rebate Max Amount"

    def get_queryset(self, request):
        return GoElectricRebateApplication.objects.all()

    def get_inlines(self, request, obj=None):
        return get_inlines(obj)


@admin.register(GoElectricRebateApplicationWithFailedEmail)
class GoElectricRebateApplicationWithFailedEmailAdmin(ITVRModelAdminStringent):
    search_fields = ["drivers_licence", "id", "status", "last_name"]
    exclude = (
        "sin",
        "doc1",
        "doc2",
        "user",
        "tax_year",
        "consent_personal",
        "consent_tax",
        "is_legacy",
    )
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "status",
        "email",
        "user_is_bcsc",
        "address",
        "city",
        "postal_code",
        "drivers_licence",
        "date_of_birth",
        "application_type",
        "doc1_tag",
        "doc2_tag",
        "confirmation_email_success",
        "spouse_email_success",
        "reason_for_decline",
        "created",
        "approved_on",
        "not_approved_on",
    )

    def get_queryset(self, request):
        return GoElectricRebateApplication.objects.filter(
            Q(confirmation_email_success=False) | Q(spouse_email_success=False)
        )


@admin.register(DriverLicenceEditableGoElectricRebateApplication)
class DriverLicenceEditableGoElectricRebateApplicationAdmin(ITVRModelAdmin):
    search_fields = ["drivers_licence", "id", "status", "last_name"]
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
        "reason_for_decline",
    )
    # drivers_licence will be included in the form as an editable field
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "status",
        "email",
        "user_is_bcsc",
        "date_of_birth",
        "tax_year",
        "is_legacy",
        "confirmation_email_success",
        "spouse_email_success",
        "created",
        "approved_on",
        "not_approved_on",
    )

    def change_view(self, request, object_id, form_url="", extra_context=None):
        if "edit_drivers_licence" in request.POST:
            return self.edit_drivers_licence(
                request, object_id, form_url, extra_context
            )
        return super().change_view(request, object_id, form_url, extra_context)

    def response_change(self, request, obj):
        ret = super().response_change(request, obj)
        if "edit_drivers_licence" in request.POST:
            new_dl = obj.drivers_licence
            if equivalent_drivers_licence_number_found(new_dl, obj.id):
                raise Exception
            rebates = list(GoElectricRebate.objects.filter(application__id=obj.id))
            if len(rebates) == 1:
                rebate = rebates[0]
                ncda_id = rebate.ncda_id
                rebate.drivers_licence = new_dl
                rebate.save()
                if ncda_id is not None:
                    update_rebate(ncda_id, {"Title": new_dl})
            elif len(rebates) > 1:
                raise Exception
        return ret

    @transaction.atomic
    def edit_drivers_licence(self, request, object_id, form_url, extra_context):
        application = GoElectricRebateApplication.objects.get(id=object_id)
        dl_history_entry = DriverLicenceHistory(
            drivers_licence=application.drivers_licence, application=application
        )
        dl_history_entry.save()
        return super().change_view(request, object_id, form_url, extra_context)


@admin.register(ChangeRedeemedGoElectricRebateApplication)
class ChangeRedeemedGoElectricRebateApplicationAdmin(ITVRModelAdmin):
    search_fields = ["drivers_licence", "id", "status", "last_name"]
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
        "reason_for_decline",
    )
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "status",
        "email",
        "user_is_bcsc",
        "drivers_licence",
        "date_of_birth",
        "tax_year",
        "is_legacy",
        "confirmation_email_success",
        "spouse_email_success",
        "created",
        "approved_on",
        "not_approved_on",
    )

    def get_queryset(self, request):
        return GoElectricRebateApplication.objects.filter(
            Q(status=GoElectricRebateApplication.Status.REDEEMED) & Q(is_legacy=False)
        )

    def response_change(self, request, obj):
        ret = super().response_change(request, obj)
        if "change_redeemed_status_to_approved" in request.POST:
            dl = obj.drivers_licence
            obj.status = GoElectricRebateApplication.Status.APPROVED
            obj.save(update_fields=["status"])
            rebate = GoElectricRebate.objects.filter(drivers_licence=dl).first()
            if rebate:
                rebate.redeemed = False
                rebate.save(update_fields=["redeemed", "modified"])
                ncda_id = rebate.ncda_id
                if ncda_id is not None:
                    update_rebate(ncda_id, {"Status": "Not-Redeemed"})
        return ret


@admin.register(ExpiredGoElectricRebateApplication)
class ExpiredGoElectricRebateApplicationAdmin(ITVRModelAdmin):
    form = ExtendExpiryForm
    search_fields = ["drivers_licence", "id", "last_name"]
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
        "reason_for_decline",
    )
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "status",
        "email",
        "user_is_bcsc",
        "drivers_licence",
        "date_of_birth",
        "tax_year",
        "is_legacy",
        "confirmation_email_success",
        "spouse_email_success",
        "created",
        "approved_on",
        "not_approved_on",
    )

    def get_queryset(self, request):
        return GoElectricRebateApplication.objects.filter(
            status=GoElectricRebateApplication.Status.EXPIRED
        )

    def response_change(self, request, obj):
        ret = super().response_change(request, obj)
        if "extend_expiry_date" in request.POST:
            drivers_licence = obj.drivers_licence
            rebate_exists = GoElectricRebate.objects.filter(
                drivers_licence=drivers_licence
            ).exists()
            if rebate_exists is False:
                ncda_rebate = get_rebate_by_drivers_licence(drivers_licence, ["Title"])
                if ncda_rebate is None:
                    obj.status = GoElectricRebateApplication.Status.APPROVED
                    obj.save(update_fields=["status"])
                    rebate_amount = request.POST.get("rebate_amount")
                    last_name = obj.last_name
                    expiry_date = date.today() + timedelta(days=30)
                    ncda_data = notify(
                        drivers_licence,
                        last_name,
                        expiry_date.strftime("%m/%d/%Y"),
                        rebate_amount,
                        obj.id,
                    )
                    ncda_id = ncda_data["d"]["ID"]
                    rebate = GoElectricRebate(
                        application=obj,
                        drivers_licence=drivers_licence,
                        last_name=last_name,
                        expiry_date=expiry_date,
                        rebate_max_amount=rebate_amount,
                        redeemed=False,
                        ncda_id=ncda_id,
                    )
                    rebate.save()
                else:
                    raise Exception("There exists an associated NCDA rebate!")
            else:
                raise Exception("There exists an associated Go Elecric Rebate!")
        return ret


@admin.register(LegacyGoElectricRebateApplication)
class LegacyGoElectricRebateApplicationAdmin(ITVRModelAdminStringent):

    def has_delete_permission(self, request, obj=None):
        return admin.ModelAdmin.has_delete_permission(self, request, obj)

    search_fields = ["drivers_licence", "id"]
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
        "reason_for_decline",
    )
    readonly_fields = (
        "id",
        "last_name",
        "first_name",
        "middle_names",
        "status",
        "email",
        "user_is_bcsc",
        "drivers_licence",
        "date_of_birth",
        "tax_year",
        "is_legacy",
        "confirmation_email_success",
        "spouse_email_success",
        "created",
        "approved_on",
        "not_approved_on",
    )

    def get_queryset(self, request):
        return GoElectricRebateApplication.objects.filter(is_legacy=True)

    def render_delete_form(self, request, context):
        new_perms_lacking = set()
        perms_lacking = context.get("perms_lacking")
        if perms_lacking is not None:
            for p in perms_lacking:
                if p != "go electric rebate application":
                    new_perms_lacking.add(p)
            context["perms_lacking"] = new_perms_lacking
        return super().render_delete_form(request, context)

    def get_deleted_objects(self, objs, request):
        (
            deleted_objects,
            model_count,
            perms_needed,
            protected,
        ) = super().get_deleted_objects(objs, request)

        new_perms_needed = set()
        if perms_needed is not None:
            for p in perms_needed:
                if p != "go electric rebate application":
                    new_perms_needed.add(p)

        return (
            deleted_objects,
            model_count,
            new_perms_needed,
            protected,
        )
