from django.db import models

from main.apps.fiobanka.managers import FiobankTransactionsQuerySet


class FiobankTransactions(models.Model):
    objects = FiobankTransactionsQuerySet.as_manager()

    transaction_id = models.CharField(max_length=15, verbose_name="ID Transakce", null=False, unique=True)
    date = models.DateField(verbose_name="Datum pohybu", null=False)
    amount = models.FloatField(verbose_name="Částka", null=False)
    currency = models.CharField(max_length=3, verbose_name="Měna", null=False)
    account_number = models.CharField(max_length=255, null=True)
    account_name = models.CharField(max_length=255, null=True)
    bank_code = models.CharField(max_length=10, null=True)
    bank_name = models.CharField(max_length=255, null=True)
    constant_symbol = models.CharField(max_length=4, null=True)
    variable_symbol = models.CharField(max_length=10, null=True)
    specific_symbol = models.CharField(max_length=10, null=True)
    user_identification = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=255, null=False)
    comment = models.CharField(max_length=140, null=True)
    instruction_id = models.CharField(max_length=12, null=True)
    bic = models.CharField(max_length=11, null=True)
    recipient_message = models.CharField(max_length=140, null=True)
    processed_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "FioBank Transakce"
        verbose_name_plural = "FioBank Transakce"

    def __str__(self):
        return self.transaction_id
