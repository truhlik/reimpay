from ..managers import PatientVisitItemQuerySet
from .. import constants


def mark_reims_as_returned(qs: PatientVisitItemQuerySet):
    qs.update(payment_status=constants.STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_RETURNED)


def mark_reims_as_sent(qs: PatientVisitItemQuerySet):
    qs.update(payment_status=constants.STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_SENT)


def mark_reims_as_waiting(qs: PatientVisitItemQuerySet):
    qs.update(payment_status=constants.STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_WAITING)

