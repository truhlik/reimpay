from django.test import TestCase

from main.libraries.utils import get_account_prefix, get_account_number, get_bank_number, validate_bank_number


class UtilsTestCase(TestCase):

    def setUp(self) -> None:
        super(UtilsTestCase, self).setUp()

    def test_get_account_prefix_with_prefix(self):
        number = '123456-123456789/0800'
        self.assertEqual('123456', get_account_prefix(number))

    def test_get_account_prefix_without_prefix(self):
        number = '123456789/0800'
        self.assertEqual('', get_account_prefix(number))

    def test_get_account_number_with_prefix(self):
        number = '123456-123456789/0800'
        self.assertEqual('123456789', get_account_number(number))

    def test_get_account_number_without_prefix(self):
        number = '123456789/0800'
        self.assertEqual('123456789', get_account_number(number))

    def test_get_bank_number_with_prefix(self):
        number = '123456-123456789/0800'
        self.assertEqual('0800', get_bank_number(number))

    def test_get_bank_number_without_prefix(self):
        number = '123456789/0800'
        self.assertEqual('0800', get_bank_number(number))

    def test_validate_bank_number(self):
        number = '7998862/0800'
        self.assertTrue(validate_bank_number(number))

    def test_validate_bank_number_2(self):
        number = '7998861/0800'
        self.assertFalse(validate_bank_number(number))

    def test_validate_bank_number_3(self):
        number = '7998862/0801'
        self.assertFalse(validate_bank_number(number))

    def test_validate_bank_number_4(self):
        number = '000000-2801781408/2010'
        self.assertTrue(validate_bank_number(number))

    def test_validate_bank_number_5(self):
        number = '000001-2901781405/2010'
        self.assertFalse(validate_bank_number(number))

    def test_validate_bank_number_6(self):
        number = '000000-2901781405/02010'
        self.assertFalse(validate_bank_number(number))
