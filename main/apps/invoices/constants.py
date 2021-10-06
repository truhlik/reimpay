from django.utils.translation import ugettext_lazy as _


INVOICE_STATUS_ISSUED = 'ISSUED'
INVOICE_STATUS_PAID = 'PAID'
INVOICE_STATUS_CANCELLED = 'CANCELLED'
INVOICE_STATUS_CHOICES = (
    (INVOICE_STATUS_ISSUED, _('Issued')),
    (INVOICE_STATUS_PAID, _('Paid')),
    (INVOICE_STATUS_CANCELLED, _('Cancelled')),
)
