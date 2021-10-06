import logging
from typing import Dict, List, Tuple

from constance import config
from django.conf import settings
from django.db import models
from django.utils import timezone

from main.apps.credit.models import CreditBalance
from main.apps.fiobanka.models import FiobankTransactions
from main.apps.payments.models import Payment
from main.apps.studies.models import Study, PatientVisitItem
from main.apps.payments import constants as payment_constants
from main.apps.credit import utils as credit_utils
from main.apps.studies.utils.patient_utils import mark_patient_as_flagged
from main.apps.studies.utils.patient_visit_item_utils import mark_reims_as_returned
from main.apps.studies.utils import study_utils


logger = logging.getLogger(__name__)


def process_new_transactions():
    """ Zprocesuje transakce a vrátí Dict s transakcemea, které se zpracovali a nebo nezpracovali. """

    # vytáhnu si jen transakce do plusu, ty je nutné zprocesovat
    transactions = FiobankTransactions.objects.for_processing()

    topup_transactions_dict = _create_topup_dict(transactions)
    returned_transactions_dict = _create_returned_payments_dict(transactions)

    if len(topup_transactions_dict) > 0:
        _process_payments_studies(topup_transactions_dict)

    if len(returned_transactions_dict) > 0:
        _process_returned_payments(returned_transactions_dict)


def _create_topup_dict(transactions) -> Dict[int, List[FiobankTransactions]]:
    transactions_dict = dict()

    for transaction in transactions:
        # transakce, které mají specific symbol prázdný, tak jsou TopUp studie
        if transaction.variable_symbol and transaction.specific_symbol in [None, ""]:
            try:
                transaction_key = int(transaction.variable_symbol)
            except ValueError:
                continue
            lst = transactions_dict.get(transaction_key, [])
            lst.append(transaction)
            transactions_dict[transaction_key] = lst
    return transactions_dict


def _create_returned_payments_dict(transactions) -> Dict[int, List[FiobankTransactions]]:
    transactions_dict = dict()

    for transaction in transactions:
        # transakce, které mají specific symbol, tak jsou returned Payments
        if transaction.variable_symbol and \
                transaction.specific_symbol not in [None, ""] and \
                transaction.constant_symbol == payment_constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER:
            try:
                transaction_key = int(transaction.variable_symbol)
            except ValueError:
                continue
            lst = transactions_dict.get(transaction_key, [])
            lst.append(transaction)
            transactions_dict[transaction_key] = lst
    return transactions_dict


def _process_payments_studies(transactions_dict: Dict[int, List[FiobankTransactions]]) -> Tuple[int, int]:
    variable_symbol_list = transactions_dict.keys()

    processed_payments = 0
    study_qs = Study.objects.active().filter(variable_symbol__in=variable_symbol_list)
    for study in study_qs:
        for trans in transactions_dict[study.variable_symbol]:
            topup_credit(study, trans.amount)
            processed_payments += 1
            trans.processed_on = timezone.now()
            trans.save()
    return processed_payments, len(study_qs)


def _process_returned_payments(transactions_dict: Dict[int, List[FiobankTransactions]]) -> int:
    variable_symbol_list = transactions_dict.keys()

    process_returned = 0  # počet plateb, které jsem označil jako vrácené
    payment_qs = Payment.objects.paychecks().filter(variable_symbol__in=variable_symbol_list)
    for payment in payment_qs:
        for trans in transactions_dict[payment.variable_symbol]:  # iteruju, přes jednotlivé FioTransaction
            if payment.total_value == int(trans.amount * settings.INT_RATIO):
                mark_payment_as_returned(payment)
                process_returned += 1
                trans.processed_on = timezone.now()
                trans.save()
            else:
                # divná platba, protože sedí variabilní symboly, ale nesedí částky
                logger.info('strange incoming returned payment - value is not same as Payment.total_value.',
                            extra={
                                'variable_symbol': payment.variable_symbol,
                                'fiobank_transaction_id': trans.id, },
                            )
    return process_returned


def topup_credit(study: Study, amount: float):
    credit_utils.add_credit_to_study(study, amount)
    if study.progress_at is None and get_actual_balance(study) > config.MIN_CREDIT_FOR_LAUNCH * settings.INT_RATIO:
        study_utils.launch_study(study)
    return


def mark_payment_as_returned(payment: Payment):
    # todo need test

    # umím automaticky zpracovat jen vrácené platby převodem
    assert payment.constant_symbol == payment_constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER

    # označit Payment jako returned
    payment.returned_on = timezone.now()
    payment.save()

    # nastavím stav Reimsů, aby to viděl CRA
    reims_qs = get_reims_from_payment(payment)
    mark_reims_as_returned(reims_qs)

    # zjistím si pacienta pro tuhle platbu
    try:
        patient = reims_qs[0].patient_visit.patient
    except IndexError as e:
        logger.error('Returned payment has no associated reims.', extra={
            'payment': payment,
        })
        return

    # flagnu si pacienta, že je třeba mu změnit payment method
    mark_patient_as_flagged(patient)

    # notifikuju někoho ?
    # todo


def process_undefined_transactions():
    """ Vytáhne si nezprocesované transakce, které jsou kladné a notifikuje adminy. """

    # vytáhnu si jen transakce do plusu, ty je nutné notifikovat
    transactions = FiobankTransactions.objects.not_processed_yet().filter(amount__gte=0)
    # todo notify admins
    transactions.update(processed_on=timezone.now())


def get_reims_from_payment(payment):
    # todo need test
    cb_qs = payment.credit_balances.all().values('id')
    return PatientVisitItem.objects.filter(credit_balances__in=cb_qs)


def get_reims_from_payment_qs(payment_qs):
    return PatientVisitItem.objects\
        .filter(credit_balances__payment__in=payment_qs.values_list('id', flat=True))\
        .order_by('created_at')


def get_actual_balance(study: Study) -> int:
    """ Vrátí aktuální kredit Studie (* 10e-9). """

    cb = CreditBalance.objects.filter(study=study).last()
    return cb.balance_sum if cb is not None else 0


def get_paid(study: Study) -> int:
    """ Vrátí kolik peněz už bylo vyplaceno z kreditního účtu. """

    return CreditBalance.objects.output().filter(study=study).aggregate(sum=models.Sum('balance_amount'))['sum'] or 0
