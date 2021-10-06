from django_cron import CronJobBase, Schedule
from main.libraries.decorators import sentry_exceptions

from . import utils


class GenerateCommissions(CronJobBase):
    RUN_EVERY_MINS = 60 * 24 * 7  # 1x za týden
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cron.GenerateCommissions'

    @sentry_exceptions
    def do(self):
        utils.generate_commissions()
