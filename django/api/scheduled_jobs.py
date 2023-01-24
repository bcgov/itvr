from django_q.tasks import schedule
from django.db import IntegrityError

# trying to create a schedule with the same name as an already created schedule will raise an IntegrityError


def schedule_send_rebates_to_ncda():
    try:
        schedule(
            "api.tasks.send_rebates_to_ncda",
            100,
            name="send_rebates_to_ncda",
            schedule_type="C",
            cron="15 * * * *",
            q_options={"timeout": 1200, "ack_failure": True},
        )
    except IntegrityError:
        pass


def schedule_get_ncda_redeemed_rebates():
    try:
        schedule(
            "api.tasks.check_rebates_redeemed_since",
            name="check_rebates_redeemed_since",
            schedule_type="C",
            cron="00 22 * * *",
            include_scheduled_run_day_minus_one=True,
        )
    except IntegrityError:
        pass


def schedule_cancel_untouched_household_applications():
    try:
        schedule(
            "api.tasks.cancel_untouched_household_applications",
            name="cancel_untouched_household_applications",
            schedule_type="C",
            cron="30 22 * * *",
        )
    except IntegrityError:
        pass


def schedule_expire_expired_applications():
    try:
        schedule(
            "api.tasks.expire_expired_applications",
            50,
            name="expire_expired_applications",
            schedule_type="C",
            cron="00 23 * * *",
            q_options={"timeout": 1200, "ack_failure": True},
        )
    except IntegrityError:
        pass


def schedule_upload_verified_applications_last_24hours_to_s3():
    try:
        schedule(
            "api.tasks.upload_verified_applications_last_24hours_to_s3",
            name="upload_verified_applications_last_24hours_to_s3",
            schedule_type="C",
            cron="00 22 * * *",
        )
    except IntegrityError:
        pass


def schedule_update_applications_cra_response():
    try:
        schedule(
            "api.tasks.update_applications_cra_response",
            name="update_applications_cra_response",
            schedule_type="C",
            cron="00 21 * * *",
        )
    except IntegrityError:
        pass
