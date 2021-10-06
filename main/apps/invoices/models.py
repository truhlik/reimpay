from django.db import models

from main.libraries.models import BaseModel

from . import constants
from .managers import InvoiceQuerySet


class Invoice(BaseModel):
    objects = InvoiceQuerySet.as_manager()

    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='invoices')
    fakturoid_invoice_id = models.IntegerField(null=True, blank=True)
    fakturoid_public_url = models.URLField(null=True, blank=True)

    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    issue_date = models.DateField()
    amount = models.PositiveIntegerField()
    status = models.CharField(choices=constants.INVOICE_STATUS_CHOICES, default=constants.INVOICE_STATUS_ISSUED, max_length=32)

    class Meta:
        verbose_name = 'invoice'
        verbose_name_plural = 'invoices'

    def __str__(self):
        return self.invoice_number if self.invoice_number else str(self.id)

    def is_owner(self, user):
        return user.company == self.company

    def can_be_edit(self):
        return False

    def can_be_deleted(self):
        return False

