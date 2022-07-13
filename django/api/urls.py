from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.viewsets.application_form import ApplicationFormViewset
from api.viewsets.household_member import HouseholdMemberApplicationViewset


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
