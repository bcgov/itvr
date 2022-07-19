from django_q.tasks import schedule
from django_q.models import Schedule


def schedule_exists(func_name):
    return Schedule.objects.filter(func__exact=func_name).exists()


def schedule_get_ncda_redeemed_rebates():
    task_name = "api.tasks.check_rebates_redeemed_since"
    if not schedule_exists(task_name):
        schedule(task_name, None, task_name, schedule_type="D")


def schedule_cancel_initiated_household():
    task_name = "api.tasks.cancel_household_applications_initiated_status"
    if not schedule_exists(task_name):
        schedule(task_name, schedule_type="D")
