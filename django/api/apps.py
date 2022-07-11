from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from . import settings
import sys


class ApiConfig(AppConfig):
    name = "api"
    verbose_name = "Submitted Rebate Applications"

    def ready(self):
        import api.signal_receivers
        from api.scheduled_jobs import schedule_get_ncda_redeemed_rebates

        if settings.RUN_JOBS and "qcluster" in sys.argv:
            schedule_get_ncda_redeemed_rebates()


class ITVRAdminConfig(AdminConfig):
    default_site = "api.site.ITVRAdminSite"
