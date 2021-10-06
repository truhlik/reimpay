from django.utils.translation import ugettext_lazy as _


PAYMENT_TYPE_BANK_TRANSFER = 'BANK'
PAYMENT_TYPE_POST_OFFICE = 'POST'

PAYMENT_TYPE_CHOICES = (
    (PAYMENT_TYPE_BANK_TRANSFER, _('bank transfer')),
    (PAYMENT_TYPE_POST_OFFICE, _('czech Post payment order (cash)')),
)
