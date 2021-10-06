import datetime

from constance import config
from django_cron import CronJobBase, Schedule
from main.libraries.decorators import sentry_exceptions

from . import utils


class GeneratingPayments(CronJobBase):
    RUN_AT_TIMES = ['00:01']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'cron.GeneratingPayments'

    @sentry_exceptions
    def do(self):
        # platby generuju jenom jeden den v měsíci
        # nebo pokud je hodina větší než 0 => spuštěno s force=True
        now = datetime.datetime.today()
        if now.day == config.PAYMENT_GENERATION_DAY or now.hour > 0:
            utils.generate_payments()  # vygeneruje objekty Payments
            utils.send_payments()  # vygeneruje platební příkazy na FIO
