from django.db.models import Sum

from main.apps.studies.models import Study, Site, Arm, Patient, Visit, PatientVisitItem
from main.apps.studies.utils import get_patient_append_visit_url, has_patient_visit


class StatsService(object):

    def __init__(self, study: Study):
        self.study = study


def create_stats(study: Study):

    site_dct = {}
    for site in Site.objects.active().filter(study=study).order_by('title'):
        arm_dct = {}
        for arm in Arm.objects.filter(study=study).order_by('title'):
            arm_patients = []

            visit_titles = False
            for patient in Patient.objects.filter(arm=arm, site=site).order_by('number'):
                visit_title_lst = ['Add visit']
                patient_visit = [get_patient_append_visit_url(patient)]
                patient_total = 0

                for visit in Visit.objects.filter(arm=arm).order_by('order'):

                    # přidám při první iteraci titulky sloupečků (názvy visit) - udělám si zde list
                    if visit_titles is False:
                        visit_title_lst.append(visit.title)

                    # pokud daný pacient nenavštívil visitu, tak vlož "-"
                    if not has_patient_visit(patient, visit):
                        patient_visit.append('-')
                    # pokud navštívil visitu, tak spočítej reims
                    else:
                        sum = PatientVisitItem.objects\
                            .filter(approved=True, patient_visit__patient=patient, patient_visit__visit=visit)\
                            .aggregate(sum=Sum('visit_item__study_item__price'))['sum'] or 0
                        patient_total += sum

                        patient_visit.append(sum)

                # přidám při první iteraci titulky sloupečků (názvy visit) - list ze shora vložím
                if visit_titles is False:
                    visit_title_lst.append('Total')
                    arm_patients.append({'Patient': visit_title_lst})
                    visit_titles = True

                patient_visit.append(patient_total)
                arm_patients.append({patient.number: patient_visit})

            if len(arm_patients) > 0:
                arm_dct[arm.title] = arm_patients

        if len(arm_dct) > 0:
            site_dct[site.title] = arm_dct

    return site_dct
