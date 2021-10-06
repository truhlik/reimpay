from django.db import models
from django.utils import timezone

from . import constants


class PaymentQuerySet(models.QuerySet):

    def fee(self):
        """ Vrátí všechny platby, které jsou za poplatky. """
        return self.filter(constant_symbol__in=[
            constants.PAYMENT_TYPE_CONSTANT_FEE_POST_OFFICE,
            constants.PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER]
        )

    def commissions(self):
        """ Vrátí všechny platby, které jsou za provize. """
        return self.filter(constant_symbol=constants.PAYMENT_TYPE_CONSTANT_COMMISSION)

    def delivered(self):
        """ Vrátí všechny platby, které ještě nebyly doručené pacientům. """

        # za doručené považujeme všechny platby, které byly odeslané před 30 a nebyly vrácené nebo
        # byly znovu poslané
        dt = timezone.now() - timezone.timedelta(days=30)
        return self.filter(
            models.Q(sent_on__isnull=False, sent_on__lte=dt, returned_on__isnull=True) |
            models.Q(resent_on__isnull=False)
        )

    def not_delivered(self):
        """ Vrátí všechny platby, které ještě nebyly doručené pacientům. """

        # za NEdoručené považujeme všechny platby, které nebyly odeslané znovu a byly odeslané v posledních 30 dnech
        # nebo byly vrácené
        dt = timezone.now() - timezone.timedelta(days=30)
        return self.filter(resent_on__isnull=True)\
            .filter(
            models.Q(models.Q(sent_on__gt=dt) | models.Q(sent_on__isnull=True)) |
            models.Q(returned_on__isnull=False)
        )

    def not_sent(self):
        """ Vrátí všechny platby, které ještě nebyly odeslané. """
        return self.filter(sent_on__isnull=True)

    def for_patient(self, patient):
        return self.filter(credit_balances__reims__patient_visit__patient=patient).distinct()

    def paychecks(self):
        """ Vrátí všechny platby, které jsou za výplaty. """
        return self.filter(constant_symbol__in=[
            constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER,
            constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE]
        )

    def returned(self):
        return self.filter(returned_on__isnull=False)
