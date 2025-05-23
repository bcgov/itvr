from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from . import settings
import sys


class ApiConfig(AppConfig):
    name = "api"
    verbose_name = "Submitted Rebate Applications"

    def ready(self):
        import api.signal_receivers
        import api.monkey_patches.itvr_django_q.cluster
        from api.scheduled_jobs import (
            schedule_send_rebates_to_ncda,
            schedule_get_ncda_redeemed_rebates,
            schedule_expire_expired_applications,
        )

        if settings.RUN_JOBS and "qcluster" in sys.argv:
            schedule_send_rebates_to_ncda()
            schedule_get_ncda_redeemed_rebates()
            schedule_expire_expired_applications()


class ITVRAdminConfig(AdminConfig):
    default_site = "api.site.ITVRAdminSite"
