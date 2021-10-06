from django.db import models

from . import constants


class CreditBalanceQuerySet(models.QuerySet):

    def get_balance_amount_sum(self) -> int:
        return self.aggregate(sum=models.Sum('balance_amount'))['sum']

    def paychecks(self):
        return self.filter(balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)

    def topups(self):
        return self.filter(balance_type=constants.CREDIT_BALANCE_TOPUP)

    def commissions(self):
        # todo need test
        return self.filter(balance_type=constants.CREDIT_BALANCE_COMMISSION)

    def post_office_fee(self):
        # todo need test
        return self.filter(balance_type=constants.CREDIT_BALANCE_POST_OFFICE_FEE)

    def bank_transfer_fee(self):
        # todo need test
        return self.filter(balance_type=constants.CREDIT_BALANCE_BANK_TRANSFER_FEE)

    def fee(self):
        # todo need test
        return self.filter(balance_type__in=[constants.CREDIT_BALANCE_POST_OFFICE_FEE,
                                             constants.CREDIT_BALANCE_BANK_TRANSFER_FEE])

    def for_invoice(self):
        """ Vrátí všechny credits, které se budou fakturovat. """

        return self.filter(balance_type__in=[
            constants.CREDIT_BALANCE_BANK_TRANSFER_FEE,
            constants.CREDIT_BALANCE_COMMISSION,
            constants.CREDIT_BALANCE_POST_OFFICE_FEE,
        ])

    def for_patient(self, patient):
        return self.filter(reims__patient_visit__patient=patient).distinct()

    def for_patients(self, patient_qs):
        # todo need test
        return self.filter(reims__patient_visit__patient__in=patient_qs).distinct()

    def not_invoiced(self):
        """ Vrátí všechny Invoiced, které ještě nebyly fakturované. """
        return self.filter(invoiced_on__isnull=True)

    def not_processed(self):
        return self.filter(payment__isnull=True)

    def output(self):
        return self.filter(balance_type__in=[
            constants.CREDIT_BALANCE_COMMISSION,
            constants.CREDIT_BALANCE_PATIENT_PAYCHECK,
            constants.CREDIT_BALANCE_BANK_TRANSFER_FEE,
            constants.CREDIT_BALANCE_POST_OFFICE_FEE,
        ])

    def owner(self, user):
        if user.is_anonymous:
            return self.none()
        if user.has_admin_role():
            return self.filter(study__company=user.company)
        else:
            return self.filter(study__sites__cra=user)

    def without_commission(self):
        return self.filter(commission__isnull=True)
