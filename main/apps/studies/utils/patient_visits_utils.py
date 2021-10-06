from typing import Optional

from django.db import models

from main.apps.studies.models import Arm, Visit, PatientVisit, Patient

from .. import constants
from ..managers import VisitQuerySet, VisitItemQuerySet


def can_change_visit_type_for_patient_visit(patient_visit: PatientVisit, patient: Patient, visit_type: str) -> bool:
    # vytvářím
    if patient_visit is None:
        return can_have_next_visit(patient, visit_type)
    else:
        # zatím nepodporuju editaci
        return False

    # # edituju patient visit
    # else:
    #     # nedošlo ke změně visit type, tak vrať True
    #     if patient_visit.visit.visit_type == visit_type:
    #         return True
    #
    #     # nemám visit type, takže ho vlastně nebudu měnit, takže můžu vrátit True
    #     if visit_type is None:
    #         return True
    #
    #     # mám visit type, tak musím respektovat přání změnit Visit
    #     else:
    #         return can_change_to_visit_type(patient_visit, visit_type)


def can_change_to_visit_type(patient_visit: PatientVisit, visit_type: str) -> bool:
    """ Vrátím zda může změnit daný visit type pro daný patient_visit. """
    assert patient_visit.visit.visit_type == visit_type

    patient = patient_visit.patient

    if visit_type == constants.STUDY_VISIT_TYPE_DISCONTINUAL:
        # na Discontinual mohou změnit vždycky
        return True

    elif visit_type == constants.STUDY_VISIT_TYPE_UNSCHEDULED:
        # pokud nepřekračuje počet max number, tak mu dovolím udělat unscheduled
        # return patient.patient_visits.discontinual().count() < patient.arm.discontinual_visit.number
        return True

    else:  # REGULAR
        visit = get_next_patient_visit(patient)
        # na regular mohu měnit pouze pokud nějaká REGULAR existuje
        if visit and visit_type == constants.STUDY_VISIT_TYPE_REGULAR:
            return True
        return False


def can_have_next_visit(patient: Patient, visit_type: str):
    if visit_type == constants.STUDY_VISIT_TYPE_UNSCHEDULED:
        # pokud nepřekračuje počet max number, tak mu dovolím udělat discontinual
        # return patient.patient_visits.discontinual().count() < patient.arm.discontinual_visit.number

        # umožním mu UNSCHEDULED pouze pokud má v plánu jakoukoliv scheduled
        return can_have_next_scheduled_visit(patient)

    elif visit_type == constants.STUDY_VISIT_TYPE_DISCONTINUAL:
        next_visit = get_next_patient_visit(patient)
        # když chce DISCONTINUAL, tak mu jí umožním pokud mám jakokoliv next scheduled (nemá již discontinual hotovou)
        return next_visit is not None
    else:
        next_visit = get_next_patient_visit(patient)
        return next_visit.visit_type == constants.STUDY_VISIT_TYPE_REGULAR if next_visit else False


def can_have_next_scheduled_visit(patient: Patient) -> bool:
    """ Vrátí zda pacient může mít další visitu. """
    # return patient.next_visit is not None
    return get_next_patient_visit(patient) is not None


def get_next_patient_visit(patient: Patient) -> Optional[Visit]:
    """ Vrátí logicky následující visitu pro pacienta. """

    visit = get_last_scheduled_visit(patient)
    if visit is None:
        return get_first_scheduled_visit_for_arm(patient.arm)
    if visit.visit_type == constants.STUDY_VISIT_TYPE_DISCONTINUAL:
        return None
    else:
        return get_next_visit_from_visit(visit)


def get_last_scheduled_visit(patient: Patient):
    previous_visits = patient.patient_visits.all().select_related('visit__arm').order_by('-created_at')
    return _get_last_scheduled_visit(previous_visits)


def _get_last_scheduled_visit(previous_visits: [PatientVisit]) -> Optional[Visit]:
    """ Vrátí první visitu ze seznamu, která je SCHEDULED (je buď regular nebo discountinual) """

    for pv in previous_visits:
        if pv.visit.visit_type == constants.STUDY_VISIT_TYPE_UNSCHEDULED:
            continue
        else:
            return pv.visit
    return None


def get_first_scheduled_visit_for_arm(arm: Arm):
    """ Vrátí první visitu z Armu. """
    return arm.visits.active().scheduled().order_by('order').first()


def get_next_visit_from_visit(visit: Visit) -> Visit:
    """ Vrátí následující Visit po zadané visitě (regular nebo discontinuation). """
    assert visit.visit_type in constants.STUDY_VISIT_TYPE_REGULAR
    return visit.arm.visits.active().scheduled().filter(order__gt=visit.order).order_by('order').first()


def filter_available_visit_items(qs: VisitItemQuerySet, patient_id: int, visit_type=None, next_only=True):
    """ Vyfiltruje všechny VisitItems podle daného visit_type, které může v tento pacient mít."""

    assert patient_id is not None

    if visit_type is None:
        visit_type = [
            constants.STUDY_VISIT_TYPE_UNSCHEDULED,
            constants.STUDY_VISIT_TYPE_DISCONTINUAL,
            constants.STUDY_VISIT_TYPE_REGULAR
        ]

    patient = Patient.objects.filter(id=patient_id).first()
    if patient is None:
        return qs.none()

    visit = get_last_scheduled_visit(patient)
    qs = qs.filter(visit__arm=patient.arm,
                   visit__order__gt=visit.order if visit else -1)  # pokud visit je None, tak chci prvni visitu

    # pokud mám zadaný list visit_type, tak filtruju přes více typů
    if isinstance(visit_type, (list, tuple)):
        qs = qs.filter(visit__visit_type__in=visit_type)
    else:
        qs = qs.filter(visit__visit_type=visit_type)

    # vyfiltruju pouze následující v pořadí, tzv. REGULAR tam bude jen 1x
    if next_only:
        qs = qs.annotate(min_order=models.Min('visit__order'))
        min_order = qs.aggregate(min_order=models.Min('visit__order'))['min_order']  # todo rewrite to subquery
        qs = qs.filter(
            models.Q(visit__order=min_order) |
            models.Q(visit__order=constants.STUDY_VISIT_DISCONTINUAL_ORDER) |
            models.Q(visit__order=constants.STUDY_VISIT_UNSCHEDULED_ORDER)
        )
    return qs.order_by('visit__order')


def filter_available_visits(qs: VisitQuerySet, patient_id: int, visit_type=None, next_only=True):
    """ Vyfiltruje všechny Visit podle daného visit_type, které může v budoucnu navštívit tento pacient."""

    assert patient_id is not None

    if visit_type is None:
        visit_type = [
            constants.STUDY_VISIT_TYPE_UNSCHEDULED,
            constants.STUDY_VISIT_TYPE_DISCONTINUAL,
            constants.STUDY_VISIT_TYPE_REGULAR
        ]

    patient = Patient.objects.filter(id=patient_id).first()
    if patient is None:
        return qs.none()

    visit = get_last_scheduled_visit(patient)
    qs = qs.filter(arm=patient.arm,
                   order__gt=visit.order if visit else -1)  # pokud visit je None, tak chci prvni visitu

    # pokud mám zadaný list visit_type, tak filtruju přes více typů
    if isinstance(visit_type, (list, tuple)):
        qs = qs.filter(visit_type__in=visit_type)
    else:
        qs = qs.filter(visit_type=visit_type)

    # vyfiltruju pouze následující v pořadí, tzv. REGULAR tam bude jen 1x
    if next_only:
        min_order = qs.aggregate(min_order=models.Min('order'))['min_order']  # todo rewrite to subquery
        qs = qs.filter(
            models.Q(order=min_order) |
            models.Q(order=constants.STUDY_VISIT_DISCONTINUAL_ORDER) |
            models.Q(order=constants.STUDY_VISIT_UNSCHEDULED_ORDER)
        )
    return qs.order_by('order')


def get_patient_available_visits(patient: Patient):
    return filter_available_visits(Visit.objects.active(), patient.id, next_only=True)


def get_unscheduled_visits(patient: Patient):
    return PatientVisit.objects.filter(patient=patient, visit__visit_type=constants.STUDY_VISIT_TYPE_UNSCHEDULED)


def can_delete_patient_visit(patient_visit: PatientVisit):
    """ Můžu smazat PV pouze pokud nemá žádný approved Reim. """
    return patient_visit.d_reim_approved is False


def has_patient_visit(patient: Patient, visit: Visit) -> bool:
    """ Vrátí zda daný pacient navštívil danou visitu. """
    return PatientVisit.objects.filter(patient=patient, visit=visit).exists()
