from django_extensions.management.jobs import HourlyJob


class Job(HourlyJob):
    help = "My sample job."

    def execute(self):
        # executing empty sample job
        file = open('cron.log','a')
        file.write('Cron has run')
        file.close()
        pass
