import datetime
import time

from django.test import TestCase
from mock import patch

from .. import utils


class FiobankUtilsTestCase(TestCase):

    def setUp(self) -> None:
        super(FiobankUtilsTestCase, self).setUp()

    def test_create_abo_payments(self):
        date = datetime.date.today().strftime('%d%m%y')
        with patch('time.time') as mock_time:
            mock_time.return_value = 1234567890
            self.maxDiff = None

            payments = [
                {
                    'bank_account_from': '2001476165/2010',
                    'bank_account_to': '1426120143/0800',
                    'value': 300,
                    'variable_symbol': 1234567890,
                    'specific_symbol': 0,
                    'constant_symbol': 610,
                },
                {
                    'bank_account_from': '2001476165/2010',
                    'bank_account_to': '1426120143/0800',
                    'value': 500,
                    'variable_symbol': 1234567890,
                    'specific_symbol': 0,
                    'constant_symbol': 610,
                },
            ]
            abo = utils.create_abo_payments(payments)

            dataa = "UHL1{}REIMPAY             0000000000001999000000000000\r\n"\
                    "1 1501 001000 2010\r\n"\
                    "2 000000-2001476165 000000000080000 {}\r\n"\
                    "000000-1426120143 000000000030000 1234567890 08000610 0000000000 AV:\r\n"\
                    "000000-1426120143 000000000050000 1234567890 08000610 0000000000 AV:\r\n"\
                    "3 +\r\n"\
                    "5 +\r\n"\
                    "".format(date, datetime.date.today().strftime('%d%m%y'))
            self.assertEqual(dataa, abo)

    def test_create_abo_payments_without_specific(self):
        date = datetime.date.today().strftime('%d%m%y')
        with patch('time.time') as mock_time:
            mock_time.return_value = 1234567890
            self.maxDiff = None

            payments = [
                {
                    'bank_account_from': '2001476165/2010',
                    'bank_account_to': '1426120143/0800',
                    'value': 300,
                    'variable_symbol': 1234567890,
                    'constant_symbol': 610,
                },
                {
                    'bank_account_from': '2001476165/2010',
                    'bank_account_to': '1426120143/0800',
                    'value': 500,
                    'variable_symbol': 1234567890,
                    'constant_symbol': 610,
                },
            ]
            abo = utils.create_abo_payments(payments)

            dataa = "UHL1{}REIMPAY             0000000000001999000000000000\r\n"\
                    "1 1501 001000 2010\r\n"\
                    "2 000000-2001476165 000000000080000 {}\r\n"\
                    "000000-1426120143 000000000030000 1234567890 08000610 0000000000 AV:\r\n"\
                    "000000-1426120143 000000000050000 1234567890 08000610 0000000000 AV:\r\n"\
                    "3 +\r\n"\
                    "5 +\r\n"\
                    "".format(date, datetime.date.today().strftime('%d%m%y'))
            self.assertEqual(dataa, abo)