from django.dispatch import receiver

from main.apps.studies.models import PatientVisitItem

from ..utils import create_credit_balance_from_reim
from ...studies.signals import approved


@receiver(approved, sender=PatientVisitItem)
def create_credit_balance(sender, instance: PatientVisitItem, **kwargs):
    create_credit_balance_from_reim(instance)
