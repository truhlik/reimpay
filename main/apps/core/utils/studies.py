from typing import Optional

from constance import config

from main.apps.core.utils import get_actual_balance
from main.apps.credit.models import CreditBalance
from main.apps.credit import constants as credit_constants
from main.apps.payments.models import Payment
from main.apps.payments import constants as payment_constants
from main.apps.studies.models import Study
from main.apps.studies import constants as study_constants


def close_studies():  # todo need test
    """ Projde všechny studie ve stavu Billing a pokud je lze uzavřít, tak je uzavře. """
    study_qs = Study.objects.filter(status=study_constants.STUDY_STATUS_BILLING)
    for study in study_qs:
        if can_study_be_closed(study):
            close_study(study)


def can_study_be_closed(study: Study) -> bool:  # todo need test
    """ Vrátí zda dané studie může být uzavřená. """

    # pokud existuje nějaká neodeslaná platba
    if Payment.objects.filter(study=study).not_delivered().exists():
        return False

    # pokud existuje nějaký Credit nevyfakturovaný
    if CreditBalance.objects.filter(study=study).for_invoice().not_invoiced().exists():
        return False

    return True


def close_study(study: Study):  # todo need test
    sum_credit = get_actual_balance(study)

    # pokud zbývá nějaký kredit, tak vytvoř platbu pro převod kreditu
    # a vytvoř finální credit balance
    if sum_credit > 0:
        payment = create_final_payment(study, sum_credit)
        create_final_credit_balance(payment)

    study.status = study_constants.STUDY_STATUS_CLOSED
    study.save()


def create_final_payment(study: Study, sum_credit: int) -> Optional[Payment]:  # todo need test
    """ Vytvoří Payment objekt z . """

    payment = Payment(
        study=study,
        total_value=sum,
        specific_symbol=None,
        variable_symbol=study.variable_symbol,
        constant_symbol=payment_constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_TOPDOWN,
        bank_account_from=config.BANK_ACCOUNT_CREDIT,
        bank_account_to=study.bank_account,
        vat_rate=0)

    payment.save()
    payment.specific_symbol = payment.id
    payment.save(update_fields=['specific_symbol'])

    return payment


def create_final_credit_balance(payment: Payment):  # todo need test
    """ Vytvoří finální CreditBalance, který by měl srovnat kredit na nulu. """

    credit = CreditBalance(
        study=payment.study,
        item_amount=payment.total_value * (-1),
        balance_type=credit_constants.CREDIT_BALANCE_TOPDOWN,
        payment=payment,
        vat_rate=0,
    )
    credit.save()
