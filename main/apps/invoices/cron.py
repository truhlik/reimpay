import datetime

from django_cron import CronJobBase, Schedule

from main.libraries.decorators import sentry_exceptions
from . import utils


class GenerateInvoices(CronJobBase):
    RUN_AT_TIMES = ['00:01']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'cron.GenerateInvoices'

    @sentry_exceptions
    def do(self):
        now = datetime.datetime.now()

        # faktury generuji jen první den v měsíci
        # nebo pokud je aktuální hodina větší než 0 => spuštěno s force=True
        if now.day == 1 or now.hour > 0:
            utils.generate_invoices()
