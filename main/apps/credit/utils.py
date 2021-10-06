import csv

from django.conf import settings

from .managers import CreditBalanceQuerySet
from .models import CreditBalance
from . import constants
from ..core.functions import get_vat_rate_int
from ..studies.models import Study, PatientVisitItem


def add_credit_to_study(study: Study, amount: float) -> CreditBalance:
    """
    Vytvoří CreditBalance pro danou studii.

    :param study: FK na studii
    :param amount: částka k připsání
    """
    # vytvořit nový CreditBalance do plusu
    cb = CreditBalance(
        study=study,
        balance_type=constants.CREDIT_BALANCE_TOPUP,
        item_amount=amount * settings.INT_RATIO,
        vat_rate=0
    )
    cb.save()
    return cb


def get_patient_from_credit(credit: CreditBalance):
    """ Vrátí objekt pacienta z dané platby. """
    assert credit.balance_type in [constants.CREDIT_BALANCE_PATIENT_PAYCHECK]
    pvi = credit.reims.first()
    return pvi.patient_visit.patient if pvi is not None else None


def create_credit_balance_from_reim(item: PatientVisitItem):
    """ Vytvoří CreditBalance (výplatu) z Reimu. """

    _create_paycheck_balance(item)  # vytváříme jenom Paycheck balance


def _create_paycheck_balance(item: PatientVisitItem):
    """ Vytvoří CreditBalance - výplata pacienta z Reimu. """

    cb = CreditBalance(
        study=item.patient_visit.study,
        item_amount=(item.visit_item.study_item.price * -1) * settings.INT_RATIO,
        balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK,
        vat_rate=0,
    )
    cb.save()
    cb.reims.set([item])


def _create_commission_balance(study: Study, item_qs: CreditBalanceQuerySet):
    """ Vytvoří CreditBalance - provize z Reimu. """

    if len(item_qs) == 0:
        return

    amount_sum = item_qs.get_balance_amount_sum()
    if amount_sum == 0:
        return

    balance_amount = (amount_sum / 100) * study.commission  # dělím 100, protože commision je v procentech (int)

    cb = CreditBalance(
        study=study,
        item_amount=balance_amount,
        balance_type=constants.CREDIT_BALANCE_COMMISSION,
        vat_rate=get_vat_rate_int(),
    )
    cb.save()
    item_qs.update(commission=cb)


def generate_commissions():
    """ Vygeneruje CreditBalance pro všechny studie za poslední týden. """

    # vytáhni si všechny aktivní studie
    study_qs = Study.objects.active()

    for study in study_qs:
        generate_commission_for_study(study)


def generate_commission_for_study(study: Study):
    """ Vytvoří CreditBalance pohyby za provize. """
    cb_qs = CreditBalance.objects.filter(study=study).paychecks().without_commission()
    _create_commission_balance(study, cb_qs)


def get_csv_export(file_obj, queryset: CreditBalanceQuerySet):
    writer = csv.writer(file_obj)
    writer.writerow(['date', 'sum', 'without VAT', 'VAT', 'type'])
    for item in queryset:
        writer.writerow([item.created_at.strftime('%Y-%m-%d'),
                         item.balance_amount / settings.INT_RATIO,
                         item.item_amount / settings.INT_RATIO,
                         item.vat_amount / settings.INT_RATIO,
                         item.get_balance_type_display(),
                         ])
    return writer
