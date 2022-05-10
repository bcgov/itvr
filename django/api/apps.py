from django.apps import AppConfig
from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        import api.signals


class ITVRAdminSite(AdminSite):
    pass

    # def get_urls(self):
    #     from django.urls import path

    #     urls = super().get_urls()
    #     urls += [path("my_view/", self.admin_view(some_view))]
    #     return urls


class ITVRAdminConfig(AdminConfig):
    default_site = "api.apps.ITVRAdminSite"
