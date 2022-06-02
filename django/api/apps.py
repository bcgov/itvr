from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        import api.signals


class ITVRAdminConfig(AdminConfig):
    default_site = "api.site.ITVRAdminSite"
