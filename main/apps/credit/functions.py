from main.apps.studies.models import Study


def get_credit_balance(study: Study):
    from main.apps.credit.models import CreditBalance
    cb = CreditBalance.objects.filter(study=study).order_by('-created_at').first()
    return cb.balance_sum if cb is not None else 0
