import random

from constance import config
from django.conf import settings
from django.db import models

from main.apps.studies.models import Study, Arm, Visit, Site, PatientVisit, Patient

from .. import constants
from ...core.constants import PAYMENT_TYPE_BANK_TRANSFER, PAYMENT_TYPE_POST_OFFICE


def launch_study(study: Study):
    study.status = constants.STUDY_STATUS_PROGRESS
    study.save()


def get_remaining_visits(study: Study):
    max_patients = max([get_expected_patients(study), get_study_patients(study)])
    avg_visits = get_avg_visits_for_study(study)
    patient_visits = PatientVisit.objects.filter(study=study).count()
    return int(max([avg_visits * max_patients - patient_visits, 0]))


def get_expected_patients(study: Study):
    """ Vrátí očekávaný počet pacientů pro studii. """

    exp_patients = Site.objects.filter(study=study).aggregate(sum=models.Sum('expected_patients'))['sum'] or 0
    return exp_patients


def get_study_patients(study: Study) -> int:
    """ Vrátí počet pacientů ve studii. """

    return Patient.objects.filter(study=study).count()


def get_avg_visits_for_study(study: Study) -> int:
    """ Vrátí průměrný počet visit v jednotlivých Armech dané studie. """

    return Arm.objects.filter(study=study)\
            .annotate(visit_count=models.Count('visits__id'))\
            .aggregate(avg_visit_count=models.Avg('visit_count'))['avg_visit_count'] or 0


def get_avg_visit_value(study: Study) -> float:
    """ Vrátí průměrnou cenu visity Pacienta pro danou studii. """

    return PatientVisit.objects.filter(study=study)\
        .annotate(sum=models.Sum('patient_visit_items__visit_item__study_item__price'))\
        .aggregate(avg_value=models.Avg('sum'))['avg_value'] or 0


def get_payment_method_fee(payment_method: str, value: int, invoice_fee: bool = False) -> int:
    """ Vrací FEE za platební metodu podle studie. Vrací hodnotu v korunách * INT_RATIO. """
    # todo need test

    # nakonci dělím 100, protože FEE je už zadané v configu v haléřích
    if payment_method == PAYMENT_TYPE_BANK_TRANSFER:
        return config.BANK_TRANSFER_FEE * settings.INT_RATIO / 100

    elif payment_method == PAYMENT_TYPE_POST_OFFICE and invoice_fee is True:
        return config.POST_OFFICE_INVOICE_FEE * settings.INT_RATIO / 100

    elif payment_method == PAYMENT_TYPE_POST_OFFICE and invoice_fee is False:
        if value <= 5000 * settings.INT_RATIO:
            return config.POST_OFFICE_FEE * settings.INT_RATIO / 100
        else:
            return config.POST_OFFICE_FEE_2 * settings.INT_RATIO / 100

    raise SystemError('unsupported payment method')


def generate_variable_symbol():
    already_exists = True
    vs = None
    while already_exists:
        vs = random.randint(1000000000, 9999999999)
        already_exists = Study.objects.filter(variable_symbol=vs).exists()
    return vs


def create_base_visit_map(study: Study):
    arm = create_arm(study)
    create_visits(study, arm)


def create_arm(study: Study) -> Arm:
    arm = Arm(
        study=study,
        title='Arm #1',
        max_unscheduled=0,
    )
    arm.save()
    return arm


def create_visits(study: Study, arm: Arm):
    unscheduled_visit = Visit(
        study=study,
        arm=arm,
        title='Unscheduled visit',
        number=0,
        visit_type=constants.STUDY_VISIT_TYPE_UNSCHEDULED,
        deleted=False,
    )
    unscheduled_visit.save()
    discontinuation_visit = Visit(
        study=study,
        arm=arm,
        title='Discontinuation (last) visit extra items',
        number=0,
        visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL,
        deleted=False,
    )
    discontinuation_visit.save()
    regular_visit = Visit(
        study=study,
        arm=arm,
        title='1. visit',
        number=0,
        visit_type=constants.STUDY_VISIT_TYPE_REGULAR,
        deleted=False,
    )
    regular_visit.save()


def get_config_empty():
    return {
        'setup': {
            'label': 'Study setup',
            'items': [
                {
                    'label': '1. Insert general information, users',
                    'completed': False,
                    'enabled': True,
                    'href': '',
                    'slug': 'general',
                },
                {
                    'label': '2. Add Reims',
                    'completed': False,
                    'enabled': False,
                    'href': '',
                    'slug': 'reims',
                },
                {
                    'label': '3. Setup Visit map',
                    'completed': False,
                    'enabled': False,
                    'href': '',
                    'slug': 'visits',
                },
                {
                    'label': '4. Add sites and print documents',
                    'completed': False,
                    'enabled': False,
                    'href': '',
                    'slug': 'sites',
                },
                # {
                #     'label': '5. Apply prelaunch lock of study',
                #     'completed': False,
                #     'enabled': False,
                #     'href': '',
                #     'slug': 'prelaunch',
                # },
                {
                    'label': '5. Top-up Initial credit',
                    'completed': False,
                    'enabled': False,
                    'href': '',
                    'slug': 'topup',
                },
            ]
        },
        'progress': {
            'label': 'Study in progress',
            'items': [
                {
                    'label': '7. Enter patients payment details',
                    'completed': False,
                    'enabled': False,
                    'href': '',
                    'slug': 'patients',
                },
                {
                    'label': '8. Reim approvals',
                    'completed': False,
                    'enabled': False,
                    'href': '',
                    'slug': 'approvals',
                },
                {
                    'label': 'Credit Top-Up (anytime)',
                    'completed': False,
                    'enabled': False,
                    'href': '',
                    'slug': 'topup',
                },
            ]
        },
        'end': {
            'label': 'Study end',
            'items': [
                {
                    'label': 'Study close-out & Reconciliation',
                    'completed': False,
                    'enabled': False,
                    'href': '',
                    'slug': 'close',
                },
            ]
        },
    }


def get_config(study: Study):
    if study is None or study._state.adding is True:
        return get_config_empty()

    return {
        'setup': {
            'label': 'Study setup',
            'items': [
                {
                    'label': '1. Insert general information, users',
                    'completed': True,
                    'enabled': False,
                    'href': '',
                    'slug': 'general',
                },
                {
                    'label': '2. Add Reims',
                    'completed': study.has_reims(),
                    'enabled': not study.has_reims(),
                    'href': '',
                    'slug': 'reims',
                },
                {
                    'label': '3. Setup Visit map',
                    'completed': study.has_visit_items(),
                    'enabled': not study.has_visit_items() and study.has_reims(),
                    'href': '',
                    'slug': 'visits',
                },
                {
                    'label': '4. Add sites and print documents',
                    'completed': study.has_sites(),
                    'enabled': not study.has_sites() and study.has_visit_items(),
                    'href': '',
                    'slug': 'sites',
                },
                # {
                #     'label': '5. Apply prelaunch lock of study',
                #     'completed': study.has_been_prelaunched(),
                #     'enabled': study.has_sites() and study.has_reims() and study.has_visit_map() and not study.has_been_prelaunched(),
                #     'href': '',
                #     'slug': 'prelaunch',
                # },
                {
                    'label': '5. Top-up Initial credit',
                    'completed': study.has_been_topup(),
                    'enabled': study.has_sites() and study.has_visit_items() and study.has_reims() and
                               study.has_visit_items() and not study.has_been_topup(),  # noqa
                    'href': '',
                    'slug': 'topup',
                },
            ]
        },
        'progress': {
            'label': 'Study in progress',
            'items': [
                {
                    'label': '7. Enter patients payment details',
                    'completed': study.is_done(),
                    'enabled': not study.is_done() and study.is_in_progress(),
                    'href': '',
                    'slug': 'patients',
                },
                {
                    'label': '8. Reim approvals',
                    'completed': study.is_done(),
                    'enabled': not study.is_done() and study.is_in_progress(),
                    'href': '',
                    'slug': 'approvals',
                },
                {
                    'label': 'Credit Top-Up (anytime)',
                    'completed': study.is_done(),
                    'enabled': not study.is_done() and study.is_in_progress(),
                    'href': '',
                    'slug': 'topup',
                },
            ]
        },
        'end': {
            'label': 'Study end',
            'items': [
                {
                    'label': 'Study close-out & Reconciliation',
                    'completed': study.is_done(),
                    'enabled': not study.is_done() and study.is_in_progress(),
                    'href': '',
                    'slug': 'close',
                },
            ]
        },
    }

