from django.db import models
from django.utils.translation import ugettext_lazy as _

from encrypted_fields import fields

from main.apps.payments.managers import PaymentQuerySet
from main.libraries.models import BaseModel

from . import constants


class PostOfficeFile(BaseModel):
    pass


class Payment(BaseModel):
    """ Reprezentuje všechny odchozí platby. """
    objects = PaymentQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', on_delete=models.CASCADE, related_name='payments')

    total_value = models.BigIntegerField(blank=True)
    url = models.URLField(blank=True, null=True)
    variable_symbol = models.BigIntegerField(blank=True, null=True)
    specific_symbol = models.BigIntegerField(null=True)
    constant_symbol = models.BigIntegerField(choices=constants.PAYMENT_TYPE_CONSTANT_SYMBOL_CHOICES)
    bank_account_from = models.CharField(max_length=255)  # musí být vždycky kreditní účet
    bank_account_to = models.CharField(max_length=255)
    vat_rate = models.PositiveSmallIntegerField()
    vat_value = models.BigIntegerField(blank=True)
    item_value = models.BigIntegerField()
    sent_on = models.DateTimeField('odesláno', blank=True, null=True)
    returned_on = models.DateTimeField('vráceno', blank=True, null=True)
    resent_on = models.DateTimeField('znovu odesláno', blank=True, null=True)

    # denormalized fields for patient address
    name = fields.EncryptedCharField(_('name'), max_length=255, blank=True, null=True)
    street = fields.EncryptedCharField(_('street'), max_length=255, blank=True, null=True)
    street_number = fields.EncryptedCharField(_('street_number'), max_length=255, blank=True, null=True)
    city = fields.EncryptedCharField(_('city'), max_length=255, blank=True, null=True)
    zip = fields.EncryptedCharField(_('zip'), max_length=255, blank=True, null=True)
    # birth_date = fields.EncryptedDateField(_('birth date'), blank=True, null=True)

    post_office = models.ForeignKey(PostOfficeFile, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Money order"
        verbose_name_plural = "Money orders"

    def _get_vat_value(self) -> int:
        # mám cenu bez DPH takže musím násobit 0.21
        if self.item_value is not None:
            # dělím 100 protože vat rate je v procentech (int)
            return int(self.item_value * self.vat_rate / 100)

        # mám cneu s DPH, takže musím dělit 1.21
        elif self.total_value is not None:
            # dělím 100 protože vat rate je v procentech (int)
            return self.total_value - int(self.total_value / (1 + (self.vat_rate / 100)))

    def save(self, *args, **kwargs):
        # spočítám vat_value
        if self.vat_value is None:
            self.vat_value = self._get_vat_value()

        # spočítám si total value pokud nemám
        if self.total_value is None and self.item_value is not None:
            self.total_value = self.item_value + self.vat_value

        # spočítám si item value pokud nemám
        if self.item_value is None and self.total_value is not None:
            self.item_value = self.total_value - self.vat_value

        super(Payment, self).save(*args, **kwargs)


class PaycheckGeneration(BaseModel):
    study = models.ForeignKey('studies.Study', on_delete=models.CASCADE, related_name='paycheck_generations')
