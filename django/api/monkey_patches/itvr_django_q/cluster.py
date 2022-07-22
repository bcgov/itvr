# Standard
import ast
from datetime import timedelta
from multiprocessing import current_process

# External
import arrow

# Django
from django import db
from django.apps.registry import apps

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Local
import django_q.tasks
from django_q.brokers import Broker, get_broker
from django_q.conf import (
    Conf,
    croniter,
    logger,
)
from django_q.models import Schedule

# module we're overriding:
from django_q import cluster


def itvr_scheduler(broker: Broker = None):
    """
    Creates a task from a schedule at the scheduled time and schedules next run
    """
    if not broker:
        broker = get_broker()
    cluster.close_old_django_connections()
    try:
        database_to_use = {"using": Conf.ORM} if not Conf.HAS_REPLICA else {}
        with db.transaction.atomic(**database_to_use):
            for s in (
                Schedule.objects.select_for_update()
                .exclude(repeats=0)
                .filter(next_run__lt=timezone.now())
                .filter(
                    db.models.Q(cluster__isnull=True) | db.models.Q(cluster=Conf.PREFIX)
                )
            ):
                args = ()
                kwargs = {}
                # get args, kwargs and hook
                if s.kwargs:
                    try:
                        # eval should be safe here because dict()
                        kwargs = eval(f"dict({s.kwargs})")
                    except SyntaxError:
                        kwargs = {}
                if s.args:
                    args = ast.literal_eval(s.args)
                    # single value won't eval to tuple, so:
                    if type(args) != tuple:
                        args = (args,)
                q_options = kwargs.get("q_options", {})
                include_scheduled_run_day_minus_one = kwargs.pop(
                    "include_scheduled_run_day_minus_one", False
                )
                if s.hook:
                    q_options["hook"] = s.hook
                # set up the next run time
                if s.schedule_type != s.ONCE:
                    next_run = arrow.get(s.next_run)
                    scheduled_run_day_minus_one = (
                        next_run - timedelta(days=1)
                    ).strftime("%Y-%m-%dT00:00:00Z")

                    while True:
                        if s.schedule_type == s.MINUTES:
                            next_run = next_run.shift(minutes=+(s.minutes or 1))
                        elif s.schedule_type == s.HOURLY:
                            next_run = next_run.shift(hours=+1)
                        elif s.schedule_type == s.DAILY:
                            next_run = next_run.shift(days=+1)
                        elif s.schedule_type == s.WEEKLY:
                            next_run = next_run.shift(weeks=+1)
                        elif s.schedule_type == s.MONTHLY:
                            next_run = next_run.shift(months=+1)
                        elif s.schedule_type == s.QUARTERLY:
                            next_run = next_run.shift(months=+3)
                        elif s.schedule_type == s.YEARLY:
                            next_run = next_run.shift(years=+1)
                        elif s.schedule_type == s.CRON:
                            if not croniter:
                                raise ImportError(
                                    _(
                                        "Please install croniter to enable cron expressions"
                                    )
                                )
                            next_run = arrow.get(
                                croniter(s.cron, cluster.localtime()).get_next()
                            )
                        if Conf.CATCH_UP or next_run > arrow.utcnow():
                            break
                    # arrow always returns a tz aware datetime, and we don't want
                    # this when we explicitly configured django with USE_TZ=False
                    s.next_run = (
                        next_run.datetime
                        if settings.USE_TZ
                        else next_run.datetime.replace(tzinfo=None)
                    )
                    s.repeats += -1
                # send it to the cluster
                scheduled_broker = broker
                try:
                    scheduled_broker = get_broker(q_options["broker_name"])
                except:  # invalid broker_name or non existing broker with broker_name
                    pass
                q_options["broker"] = scheduled_broker
                q_options["group"] = q_options.get("group", s.name or s.id)
                kwargs["q_options"] = q_options
                if include_scheduled_run_day_minus_one:
                    args = args + (scheduled_run_day_minus_one,)
                s.task = django_q.tasks.async_task(s.func, *args, **kwargs)
                # log it
                if not s.task:
                    logger.error(
                        _(
                            f"{current_process().name} failed to create a task from schedule [{s.name or s.id}]"
                        )
                    )
                else:
                    logger.info(
                        _(
                            f"{current_process().name} created a task from schedule [{s.name or s.id}]"
                        )
                    )
                # default behavior is to delete a ONCE schedule
                if s.schedule_type == s.ONCE:
                    if s.repeats < 0:
                        s.delete()
                        continue
                    # but not if it has a positive repeats
                    s.repeats = 0
                # save the schedule
                s.save()
    except Exception as e:
        logger.error(e)


cluster.scheduler = itvr_scheduler
