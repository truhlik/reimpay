import urllib

from django.urls import reverse
from django.utils import timezone

from main.libraries.functions import get_absolute_url
from ..models import Patient, Study
from .. import constants


def mark_patient_as_flagged(patient: Patient):
    patient.change_payment_request = timezone.now()
    patient.save()


def get_patients_in_progress(study: Study):
    return Patient.objects.active().filter(study=study).in_progress()


def set_patient_terminated(patient: Patient):
    patient.status = constants.STUDY_PATIENT_STATUS_TERMINATED
    patient.save()


def get_patient_append_visit_url(patient: Patient):
    return get_absolute_url(urllib.parse.unquote(reverse('frontend-patient-detail', args=(patient.id, ))))
