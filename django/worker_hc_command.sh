import os
import django

#  Set the correct path to you settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

# All django stuff has to come after the setup:
django.setup()

from django_q.monitor import Stat
from django_q.conf import Conf


class HealthCheckServer():
    def check(self):

        # Count the clusters and their status
        happy_clusters = 0
        total_clusters = 0

        for stat in Stat.get_all():
            print("11")
            total_clusters += 1
            if stat.status in [Conf.IDLE, Conf.WORKING]:
                happy_clusters += 1

        # Return 200 response if there is at least 1 cluster running,
        # and make sure all running clusters are happy
        if total_clusters and happy_clusters == total_clusters:
            print("200")
        else:
            print("500")

if __name__ == "__main__":
    a = HealthCheckServer()
    a.check()