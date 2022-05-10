from django.contrib import admin
from .models.go_electric_rebate_application import (
    GoElectricRebateApplication,
    SubmittedGoElectricRebateApplication,
)
from .models.household_member import HouseholdMember


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


@admin.register(GoElectricRebateApplication)
class GoElectricRebateApplicationAdmin(admin.ModelAdmin):
    pass


# The proxy model is used to avoid a Django limitation where a model can only
# be registered once on the admin panel. This locked down version will be used
# by government staff to verify or decline submitted applications
# by BCeID users.
@admin.register(SubmittedGoElectricRebateApplication)
class SubmittedGoElectricRebateApplicationAdmin(admin.ModelAdmin):
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

    def response_change(self, request, obj):
        ret = super().response_change(request, obj)
        if "approve_application" in request.POST:
            obj.status = GoElectricRebateApplication.Status.VERIFIED
            obj.save()
        if "reject_application" in request.POST:
            obj.status = GoElectricRebateApplication.Status.DECLINED
            obj.save()
        return ret


# class YourAdmin(admin.ModelAdmin):
#      # add the link to the various fields attributes (fieldsets if necessary)
#     readonly_fields = ('download_link',)
#     fields = (..., 'download_link', ...)

#     # add custom view to urls
#     def get_urls(self):
#         urls = super(YourAdmin, self).get_urls()
#         urls += [
#             url(r'^download-file/(?P<pk>\d+)$', self.download_file,
#                 name='applabel_modelname_download-file'),
#         ]
#         return urls

#     # custom "field" that returns a link to the custom function
#     def download_link(self, obj):
#         return format_html(
#             '<a href="{}">Download file</a>',
#             reverse('admin:applabel_modelname_download-file', args=[obj.pk])
#         )
#     download_link.short_description = "Download file"

#     # add custom view function that downloads the file
#     def download_file(self, request, pk):
#         response = HttpResponse(content_type='application/force-download')
#         response['Content-Disposition'] = 'attachment; filename="whatever.txt"')
#         # generate dynamic file content using object pk
#         response.write('whatever content')
#         return response
