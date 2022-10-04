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
            schedule_cancel_untouched_household_applications,
            schedule_expire_expired_applications,
            schedule_upload_verified_applications_last_24hours_to_s3,
            schedule_update_applications_cra_response
            
        )

        if settings.RUN_JOBS and "qcluster" in sys.argv:
            schedule_send_rebates_to_ncda()
            schedule_get_ncda_redeemed_rebates()
            schedule_cancel_untouched_household_applications()
            schedule_expire_expired_applications(),
            schedule_upload_verified_applications_last_24hours_to_s3()
            schedule_update_applications_cra_response()


class ITVRAdminConfig(AdminConfig):
    default_site = "api.site.ITVRAdminSite"
