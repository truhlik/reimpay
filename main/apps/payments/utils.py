from calendar import monthrange
from typing import List, Dict, Tuple

from constance import config
from django.conf import settings
from django.db import models
from django.utils import timezone

from main.apps.credit.models import CreditBalance
from main.apps.credit import constants as credit_constants
from main.apps.studies.models import Study, Patient
from main.apps.studies import constants as study_const
from main.apps.fiobanka import utils as fiobank_utils
from .managers import PaymentQuerySet

from .models import Payment, PaycheckGeneration, PostOfficeFile
from . import constants
from ..core.constants import PAYMENT_TYPE_BANK_TRANSFER, PAYMENT_TYPE_POST_OFFICE
from ..core.functions import get_vat_rate_int
from main.apps.studies.utils import get_payment_method_fee
from main.apps.studies.utils.patient_visit_item_utils import mark_reims_as_sent


def generate_payments():
    """ Vygeneruje odchozí platby pro všechny studie. """

    # vytáhni si všechny aktivní studie
    study_qs = Study.objects.filter(status__in=[
        study_const.STUDY_STATUS_PROGRESS, study_const.STUDY_STATUS_BILLING,
    ])

    for study in study_qs:
        _generate_payments_for_study(study)


def _generate_payments_for_study(study: Study):
    # todo need test
    """ Vygeneruje odchozí platby pro konkrétní studii. """

    _generate_commission_payment(study)  # vygeneruje Platby za provize, muzu kdykoliv a co nejdrive

    if _can_generate_paychecks(study):
        generate_payments_for_patients(study)  # vygeneruje Platby za výplaty pacientům
        PaycheckGeneration.objects.create(study=study)


def _can_generate_paychecks(study: Study):
    # paychecks platby generuju jednou za X měsíců (dle nastavení studie)
    days = get_days_from_pay_frequency(study.pay_frequency)
    dt = timezone.now() - timezone.timedelta(days=days)

    # pokud studie byla spuštěna před méně než X dny
    if study.progress_at > dt:
        return False

    # pokud poslední Paycheck proběhl před méně než X dny
    if PaycheckGeneration.objects.filter(study=study, created_at__gt=dt).exists():
        return False
    return True


def _generate_commission_payment(study: Study):
    """ Vygeneruje provize za konkrétní studii. """

    # commission můžu převádět hned na provozní účet
    qs = CreditBalance.objects.not_processed().commissions().filter(study=study)

    qs_dct = qs.aggregate(sum=models.Sum('balance_amount'), vat_rate=models.Max('vat_rate'))

    if qs_dct['sum'] and qs_dct['sum'] != 0:
        payment = Payment(
            study=study,
            total_value=(qs_dct['sum']) * (-1),
            specific_symbol=None,
            variable_symbol=study.variable_symbol,
            constant_symbol=constants.PAYMENT_TYPE_CONSTANT_COMMISSION,
            bank_account_from=config.BANK_ACCOUNT_CREDIT,
            bank_account_to=config.BANK_ACCOUNT_OPERATIONAL,
            vat_rate=qs_dct['vat_rate']
        )
        payment.save()
        payment.specific_symbol = payment.id
        payment.save()
        qs.update(payment=payment)


def generate_payments_for_patients(study: Study):
    for payment_type, const_symbol_fee in [
        (PAYMENT_TYPE_BANK_TRANSFER, constants.PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER),
        (PAYMENT_TYPE_POST_OFFICE, constants.PAYMENT_TYPE_CONSTANT_FEE_POST_OFFICE),
    ]:

        # vytáhnu si všechny pacienty s danou platební metodou
        patient_qs = Patient.objects.not_flagged()\
            .filter(study=study, payment_type=payment_type)\
            .select_related('study')

        # pro každého pacienta jdu generovat platby
        number_of_payments = 0
        fee = 0
        for patient in patient_qs:
            bank_account_to = get_bank_account_for_patient(patient)
            const_symbol = get_const_symbol_for_patient_paycheck_payment(patient)

            generated, value = _generate_paycheck_for_patient(patient, const_symbol, bank_account_to)
            # pokud jsem vygeneroval platbu, tak musím zjistit poplatek za platební metodu
            if generated:
                fee += get_payment_method_fee(payment_type, value, invoice_fee=True)

        # vygeneruju fee platbu za poplatky za platební metodu
        if fee > 0:
            _generate_payment_fee(fee,
                                  study,
                                  const_symbol_fee,
                                  get_vat_rate_int())


def _generate_payment_fee(fee: int, study: Study, payment_type: str, vat_rate: int):
    """
    Vygeneruje platbu za poplatky.
    :param fee: celková suma poplatků v háleřích
    """
    payment = Payment(
        study=study,
        total_value=fee,
        specific_symbol=None,
        variable_symbol=study.variable_symbol,
        constant_symbol=payment_type,
        bank_account_from=config.BANK_ACCOUNT_CREDIT,
        bank_account_to=config.BANK_ACCOUNT_OPERATIONAL,
        vat_rate=vat_rate
    )
    payment.save()
    payment.specific_symbol = payment.id
    payment.save()

    # musím odečíst kredit studie
    if payment_type == constants.PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER:
        credit_balance_type = credit_constants.CREDIT_BALANCE_BANK_TRANSFER_FEE
    else:
        credit_balance_type = credit_constants.CREDIT_BALANCE_POST_OFFICE_FEE
    _create_credit_fee_balance(payment, credit_balance_type)


def _create_credit_fee_balance(payment: Payment, fee_type: str):
    """ Vytvoří CreditBalance - poplatek za platební metodu. """

    cb = CreditBalance(
        study=payment.study,
        item_amount=payment.total_value * (-1),
        balance_type=fee_type,
        payment=payment,
        vat_rate=get_vat_rate_int(),
    )
    cb.save()


def _generate_paycheck_for_patient(patient, const_symbol: int, bank_account_to: str) -> Tuple[bool, int]:

    qs = CreditBalance.objects \
        .not_processed() \
        .paychecks() \
        .for_patient(patient)

    qs_dct = qs.aggregate(sum=models.Sum('balance_amount'), vat_rate=models.Max('vat_rate'))

    # musím se ještě podívat jestli nemám pro pacienta nějaké vrácené platby
    returned_payments_qs = get_returned_payments_for_patient(patient)
    p_sum = returned_payments_qs.aggregate(sum=models.Sum('total_value'))['sum']

    # sečtu částky za CreditBalance a returned Payments
    total_sum = qs_dct['sum'] if qs_dct['sum'] else 0 + p_sum if p_sum else 0

    if total_sum == 0:
        return False, 0

    payment = Payment(
        study=patient.study,
        total_value=total_sum * -1,
        specific_symbol=None,
        variable_symbol=patient.study.variable_symbol,
        constant_symbol=const_symbol,
        bank_account_from=config.BANK_ACCOUNT_CREDIT,
        bank_account_to=bank_account_to,
        vat_rate=qs_dct['vat_rate'],
        # denormalizujeme fieldy pro uzivatele
        name=patient.name,
        street=patient.street,
        street_number=patient.street_number,
        city=patient.city,
        zip=patient.zip,
    )
    payment.save()
    payment.specific_symbol = payment.id
    payment.save()

    # CreditBalance provážu s touto platbou
    qs.update(payment=payment)

    # nastavím si u vrácených plateb, že byly znovu odeslaný
    if returned_payments_qs:
        returned_payments_qs.update(resent_on=payment.created_at)

    return True, payment.total_value


def get_days_from_pay_frequency(months_count: int, date=None) -> int:
    """ Vrátí počet dní v předcházejících X měsících. """

    if date is None:
        date = timezone.now().date()

    first_day_of_current_month = date.replace(day=1)  # první den aktuálního měsíce
    last_day_of_last_month = first_day_of_current_month - timezone.timedelta(days=1)  # poslední den předcházejícího měsíce

    cummulative_days = 0

    for i in range(1, months_count + 1):
        # zjistím počet dní v předcházejícím měsíci
        _, days_in_month = monthrange(last_day_of_last_month.year, last_day_of_last_month.month)

        # přičtu si počet dní kumulativně
        cummulative_days += days_in_month

        # skočím na poslední den předcházejícího měsíce
        last_day_of_last_month = last_day_of_last_month - timezone.timedelta(days=days_in_month)

    return cummulative_days


def send_payments():
    """ Odešle vygenerované Payments na FIO a označí jako odeslané. """

    bt_data, bt_qs = generate_payment_data_without_post_office()
    po_data, po_qs = generate_payment_data_for_post_office()

    # pokud není žádná platba, tak nic nedělej
    if len(po_data + bt_data) == 0:
        return

    abo = fiobank_utils.create_abo_payments(bt_data + po_data)
    if abo is None:
        raise Exception('abo file generation failed, any account number is incorrect')

    result, error_lst = fiobank_utils.send_abo_to_fio(abo, config.FIO_BANK_TOKEN)
    if result is False:
        raise Exception('payments not send: {}'.format(str(error_lst)))

    # označím si platby jako odeslané
    mark_payments_as_sent(bt_qs)
    if len(po_qs) > 0:
        po = PostOfficeFile()
        po.save()
        mark_payments_as_sent(po_qs, po)


def mark_payments_as_sent(qs: PaymentQuerySet, post_office_obj: PostOfficeFile = None):
    # nastavím stav Reimsů, aby to viděl CRA
    from main.apps.core.utils import get_reims_from_payment_qs
    reims_qs = get_reims_from_payment_qs(qs)
    mark_reims_as_sent(reims_qs)

    # označím si Payment jako odeslané
    if post_office_obj is None:
        qs.update(sent_on=timezone.now())
    else:
        qs.update(sent_on=timezone.now(), post_office=post_office_obj)


def generate_payment_data_without_post_office() -> Tuple[List[Dict], PaymentQuerySet]:
    """ Vygeneruje platební příkazy pro všechny bankovní převody. """

    # Dělám group_by i podle variabilního symbolu, což defacto by nemělo udělat žádný GROUP_BY,
    # protože var. symbol bude jedinečný pro každou z těchto payment

    qs = Payment.objects\
        .not_sent() \
        .exclude(constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE)
    data = qs.values('bank_account_from', 'bank_account_to', 'variable_symbol', 'specific_symbol', 'constant_symbol') \
        .annotate(value=models.F('total_value') / settings.INT_RATIO) \
        .values('bank_account_from',
                'bank_account_to',
                'value',
                'variable_symbol',
                'specific_symbol',
                'constant_symbol')
    return list(data), qs


def generate_payment_data_for_post_office() -> Tuple[List[Dict], PaymentQuerySet]:
    """ Vygeneruje platební příkazy pro všechny poštovní poukázky jako jeden převod. """

    # Nedělám GROUP_BY podle specifického symbolu,
    # protože chci všechny paycheck přes ČP poslat pouze jedním platebním příkazem

    qs = Payment.objects.not_sent()\
        .filter(constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE)

    data = qs.values('bank_account_from', 'bank_account_to', 'constant_symbol')\
        .annotate(value=models.Sum('total_value') / settings.INT_RATIO)\
        .values('bank_account_from',
                'bank_account_to',
                'value',
                'variable_symbol',
                'constant_symbol').order_by('value')

    return list(data), qs


def get_returned_payments_for_patient(patient: Patient) -> PaymentQuerySet:
    return Payment.objects.for_patient(patient).returned().filter(resent_on__isnull=True)


# def generate_payments_from_returned(study: Study):
#     p_qs = Payment.objects.filter(study=study).returned().not_resent().patient_not_flagged()
#
#     for payment in p_qs:
#         create_payment_from_returned_to_patient(payment, payment.patient)
#
#
# def create_payment_from_returned_to_patient(payment: Payment, patient: Patient):
#     """ Vytvoří platbu ze současné platby. """
#
#     bank_account_to = get_bank_account_for_patient(patient)
#     const_symbol = get_const_symbol_for_patient_paycheck_payment(patient)
#
#     payment = Payment(
#         study=patient.study,
#         total_value=payment.total_value,
#         specific_symbol=None,
#         variable_symbol=patient.study.variable_symbol,
#         constant_symbol=const_symbol,
#         bank_account_from=config.BANK_ACCOUNT_CREDIT,
#         bank_account_to=bank_account_to,
#         vat_rate=payment.vat_rate,
#         patient=patient,
#     )
#     payment.save()
#     payment.specific_symbol = payment.id
#     payment.save()
#
#
def get_bank_account_for_patient(patient: Patient) -> str:
    """ Vrátí bankovní účet pacienta na kterou bude odeslána platba. """

    if patient.payment_type == PAYMENT_TYPE_POST_OFFICE:
        return config.POST_OFFICE_BANK_ACCOUNT
    else:
        return patient.payment_info


def get_const_symbol_for_patient_paycheck_payment(patient: Patient) -> int:
    """ Vrací konstatní symbol pro platbu daného pacienta. """
    if patient.payment_type == PAYMENT_TYPE_POST_OFFICE:
        return constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE
    else:
        return constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER


def generate_transfer_operational_cp(post_office_fee: int, variable_symbol: str):
    """ Vygeneruje platební příkaz pro převod z Operačního účtu na ČP. """

    data = [{
        'bank_account_from': config.BANK_ACCOUNT_OPERATIONAL,
        'bank_account_to': config.POST_OFFICE_BANK_ACCOUNT,
        'value': post_office_fee,
        'variable_symbol': variable_symbol,  # voluntary
        'specific_symbol': 0,  # v případě ČP převodu není
        'constant_symbol': 610,
    }]

    abo = fiobank_utils.create_abo_payments(data)
    if abo is None:
        raise Exception('abo file generation failed, any account number is incorrect')

    result, error_lst = fiobank_utils.send_abo_to_fio(abo, config.FIO_BANK_TOKEN_OPERATIONAL)
    if result is False:
        raise Exception('payments not send: {}'.format(str(error_lst)))
