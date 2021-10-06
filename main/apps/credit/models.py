from django.db import models
from django.utils.translation import ugettext_lazy as _

from main.libraries.models import BaseModel
from .managers import CreditBalanceQuerySet
from . import constants, functions


class CreditBalance(BaseModel):
    objects = CreditBalanceQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', verbose_name=_('study'), related_name='credit', on_delete=models.CASCADE)
    balance_type = models.CharField('typ pohybu', choices=constants.CREDIT_BALANCE_CHOICES, max_length=32)
    balance_amount = models.BigIntegerField('suma', blank=True)
    item_amount = models.BigIntegerField('bez DPH')
    vat_amount = models.BigIntegerField('DPH', blank=True)
    balance_sum = models.BigIntegerField('sumarizace kreditu', blank=True)
    reims = models.ManyToManyField('studies.PatientVisitItem', blank=True, related_name='credit_balances')
    payment = models.ForeignKey('payments.Payment', blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='credit_balances')
    commission = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='credit_balances')

    vat_rate = models.PositiveSmallIntegerField('procentuální sazba DPH')
    invoiced_on = models.DateTimeField('fakturováno', blank=True, null=True)

    class Meta:
        verbose_name = _('credit balance')
        verbose_name_plural = _('credit balances')

    def __str__(self):
        return self.balance_type

    def _get_vat_amount(self) -> int:
        if self.item_amount is not None:
            return int(self.item_amount * self.vat_rate / 100)
        elif self.balance_amount is not None:
            return int(self.balance_amount - self.balance_amount / (1 + (self.vat_rate / 100)))

    def _get_item_amount(self) -> int:
        if self.balance_amount is not None:
            return int(self.balance_amount / (1 + (self.vat_rate / 100)))

    def _get_balance_amount(self):
        return self.item_amount + self._get_vat_amount()

    def save(self, *args, **kwargs):
        # todo tady by bylo potřeba použít transakci

        # vypočtu si hodnotu DPH
        if self.balance_amount is None:
            self.balance_amount = self._get_balance_amount()

        if self.vat_amount is None:
            self.vat_amount = self._get_vat_amount()

        if self.item_amount is None:
            self.item_amount = self._get_item_amount()

        # nastavím si aktuální kredit studie
        if self.balance_sum is None:
            self.balance_sum = functions.get_credit_balance(self.study) + self.balance_amount
        super(CreditBalance, self).save(*args, **kwargs)
