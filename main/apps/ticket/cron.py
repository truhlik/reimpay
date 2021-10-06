from django_cron import CronJobBase, Schedule

from main.libraries.decorators import sentry_exceptions
from . import utils


class SendTicketsCronJob(CronJobBase):
    RUN_EVERY_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cron.SendTicketsCronJob'

    @sentry_exceptions
    def do(self):
        utils.send_tickets()

