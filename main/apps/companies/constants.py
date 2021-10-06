from django.utils.translation import ugettext_lazy as _

COMPANY_ROLE_CONSULTANT = 'CONSULTANT'
COMPANY_ROLE_SUPPLIER = 'SUPPLIER'
COMPANY_ROLE_CLIENT = 'CLIENT'

COMPANY_ROLE_CHOICES = (
    (COMPANY_ROLE_CONSULTANT, _("konzultant")),
    (COMPANY_ROLE_SUPPLIER, _('dodavatel')),
    (COMPANY_ROLE_CLIENT, _('client')),
)
