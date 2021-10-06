from django.test import TestCase
from django.utils import timezone

from model_bakery import baker

from ..models import FiobankTransactions


class FiobankTransactionsQuerySetTestCase(TestCase):

    def setUp(self) -> None:
        super(FiobankTransactionsQuerySetTestCase, self).setUp()

    def test_for_processing(self):
        baker.make(FiobankTransactions, processed_on=None, amount=1, variable_symbol='')
        baker.make(FiobankTransactions, processed_on=timezone.now(), amount=1, variable_symbol=1)
        baker.make(FiobankTransactions, processed_on=None, amount=-1, variable_symbol=1)
        f1 = baker.make(FiobankTransactions, processed_on=None, amount=1, variable_symbol=1)
        qs = FiobankTransactions.objects.for_processing()
        self.assertEqual(1, len(qs))
        self.assertEqual(f1, qs[0])

    def test_not_processed_yet(self):
        f1 = baker.make(FiobankTransactions, processed_on=None)
        baker.make(FiobankTransactions, processed_on=timezone.now())
        qs = FiobankTransactions.objects.not_processed_yet()
        self.assertEqual(1, len(qs))
        self.assertEqual(f1, qs[0])
