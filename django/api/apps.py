from django.apps import AppConfig
from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig
from .views import download_file


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        import api.signals


class ITVRAdminSite(AdminSite):
    def get_urls(self):
        from django.urls import path

        print("GETTING CUSTOM URLS")

        urls = super().get_urls()
        urls = [path("cra-download", self.admin_view(download_file))] + urls

        return urls


class ITVRAdminConfig(AdminConfig):
    default_site = "api.apps.ITVRAdminSite"
