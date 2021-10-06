from constance import config
from mock import patch
from django.test import TestCase

from ..functions import FioBankPayments
from ..models import FiobankTransactions
from . import test_data


class FiobankTransactionsQuerySetTestCase(TestCase):

    def setUp(self) -> None:
        super(FiobankTransactionsQuerySetTestCase, self).setUp()

    @patch('main.apps.fiobanka.functions.FioBank.period')
    def test_pairing(self, mock_period):
        mock_period.return_value = []
        FioBankPayments.start_pairing()
        self.assertEqual(0, len(FiobankTransactions.objects.all()))

    @patch('main.apps.fiobanka.functions.FioBank.period')
    def test_pairing_with_test_data(self, mock_period):
        config.FIO_BANK_TOKEN = 'test'
        mock_period.return_value = test_data
        FioBankPayments.start_pairing()
        self.assertEqual(25, len(FiobankTransactions.objects.all()))

    @patch('main.apps.fiobanka.functions.FioBank.period')
    def test_pairing_with_test_data_duplicate(self, mock_period):
        config.FIO_BANK_TOKEN = 'test'
        mock_period.return_value = test_data
        FioBankPayments.start_pairing()
        FioBankPayments.start_pairing()
        self.assertEqual(25, len(FiobankTransactions.objects.all()))