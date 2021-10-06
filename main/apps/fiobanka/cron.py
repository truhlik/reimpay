from django_cron import CronJobBase, Schedule
from .functions import FioBankPayments
from main.libraries.decorators import sentry_exceptions


class FioBankPairingPayments(CronJobBase):
    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cron.FioBankPairingPayments'

    @sentry_exceptions
    def do(self):
        FioBankPayments.start_pairing()
