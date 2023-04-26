from django_q.tasks import schedule
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta

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
            include_scheduled_run_time=True,
            q_options={"timeout": 1200},
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


def schedule_get_missing_redeemed_rebates():
    try:
        schedule(
            "api.tasks.get_missed_redeemed_rebates",
            "2023-03-14T00:00:00Z",
            name="get_missing_redeemed_rebates",
            schedule_type="O",
            repeats=1,
            next_run=timezone.now() + timedelta(hours=1),
            q_options={"timeout": 1200, "ack_failure": True},
        )
    except IntegrityError:
        pass
