from django_q.tasks import schedule
from django.db import IntegrityError

# trying to create a schedule with the same name as an already created schedule will raise an IntegrityError


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
            name="expire_expired_applications",
            schedule_type="C",
            cron="00 23 * * *",
        )
    except IntegrityError:
        pass
