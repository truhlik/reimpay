from django.utils.translation import ugettext_lazy as _


STUDY_STATUS_DRAFT = 'DRAFT'
STUDY_STATUS_PRELAUNCH = 'PRELAUNCH'
STUDY_STATUS_PROGRESS = 'PROGRESS'
STUDY_STATUS_BILLING = 'BILLING'
STUDY_STATUS_CLOSED = 'CLOSED'

STUDY_STATUS_CHOICES = (
    (STUDY_STATUS_DRAFT, _('draft')),
    (STUDY_STATUS_PRELAUNCH, _('prelaunch')),
    (STUDY_STATUS_PROGRESS, _('progress')),
    (STUDY_STATUS_BILLING, _('billing')),
    (STUDY_STATUS_CLOSED, _('closed')),

)


STUDY_PATIENT_STATUS_TERMINATED = 'TERMINDATED'
STUDY_PATIENT_STATUS_ACTIVE = 'ACTIVE'
STUDY_PATIENT_STATUS_CHOICES = (
    (STUDY_PATIENT_STATUS_TERMINATED, 'terminated'),
    (STUDY_PATIENT_STATUS_ACTIVE, 'active'),
)


STUDY_VISIT_TYPE_UNSCHEDULED = 'UNSCHEDULED'
STUDY_VISIT_TYPE_DISCONTINUAL = 'DISCONTINUAL'
STUDY_VISIT_TYPE_REGULAR = 'REGULAR'
STUDY_VISIT_TYPE_CHOICES = (
    (STUDY_VISIT_TYPE_UNSCHEDULED, 'UNSCHEDULED'),
    (STUDY_VISIT_TYPE_DISCONTINUAL, 'DISCONTINUAL'),
    (STUDY_VISIT_TYPE_REGULAR, 'REGULAR'),
)


STUDY_VISIT_UNSCHEDULED_ORDER = 9999
STUDY_VISIT_DISCONTINUAL_ORDER = 10000


STUDY_PATIENT_VISIT_ITEM_ORIGIN_CRA = 'CRA'
STUDY_PATIENT_VISIT_ITEM_ORIGIN_SITE = 'SITE'
STUDY_PATIENT_VISIT_ITEM_ORIGIN_CHOICES = (
    (STUDY_PATIENT_VISIT_ITEM_ORIGIN_CRA, _('CRA')),
    (STUDY_PATIENT_VISIT_ITEM_ORIGIN_SITE, _('SITE')),
)


STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_WAITING = 'WAITING'
STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_SENT = 'SENT'
STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_RETURNED = 'RETURNED'
STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_CHOICES = (
    (STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_WAITING, 'In enque for processing'),
    (STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_SENT, 'Sent'),
    (STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_RETURNED, 'Returned'),
)


STUDY_OPERATOR_CRO = 'CRO'
STUDY_OPERATOR_SPONSOR = 'SPONSOR'
STUDY_OPERATOR_CHOICES = (
    (STUDY_OPERATOR_CRO, 'CRO'),
    (STUDY_OPERATOR_SPONSOR, 'SPONSOR'),
)
