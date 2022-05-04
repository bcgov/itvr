from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.viewsets.application_form import ApplicationFormViewset
from api.viewsets.household_member import HouseholdMemberApplicationViewset

admin.site.site_header = "BC Gov ITVR"
admin.site.index_title = "Admin Panel"
admin.site.site_title = "BC Gov ITVR"


class OptionalSlashRouter(routers.DefaultRouter):
    def __init__(self):
        super().__init__()
        self.trailing_slash = "/?"


ROUTER = OptionalSlashRouter()
ROUTER.register(r"application-form", ApplicationFormViewset)
ROUTER.register(r"spouse-application", HouseholdMemberApplicationViewset)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(ROUTER.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
