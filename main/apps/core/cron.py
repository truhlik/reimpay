from django_cron import CronJobBase, Schedule
from main.libraries.decorators import sentry_exceptions

from . import utils


class FioBankProcessingPayments(CronJobBase):
    RUN_EVERY_MINS = 60
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cron.FioBankProcessingPayments'

    @sentry_exceptions
    def do(self):
        utils.process_new_transactions()  # zprocesuje nové transakce v DB
        utils.process_undefined_transactions()  # zprocesuje nezprocesované transakce v DB


class StudyCloseCron(CronJobBase):
    RUN_AT_TIMES = ['2:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'cron.StudyCloseCron'

    @sentry_exceptions
    def do(self):
        utils.close_studies()
