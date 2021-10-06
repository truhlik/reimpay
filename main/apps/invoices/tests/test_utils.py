from django.conf import settings
from django.test import TestCase
from model_bakery import baker

from main.apps.credit import constants as credit_const
from .. import utils
from ...credit.models import CreditBalance


class InvoicesTestCase(TestCase):

    def setUp(self) -> None:
        super(InvoicesTestCase, self).setUp()
        self.maxDiff = None

    def test_generate_invoice_data_simple(self):
        study = baker.make('studies.Study', number='test123')

        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE, study=study, balance_amount=-1.02 * settings.INT_RATIO, vat_rate=21)

        qs = CreditBalance.objects.filter(study__company=study.company).for_invoice()

        data = utils.generate_invoice_data(qs)
        exp_data = [
            {
                'total': 1.02,
                'balance_type': credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE,
                'study__number': 'test123',
                'vat_rate': 21,
            }
        ]
        self.assertEqual(exp_data, data)

    def test_generate_invoice_data(self):
        study = baker.make('studies.Study', number='test123')

        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_TOPUP, study=study, balance_amount=6 * settings.INT_RATIO, vat_rate=21)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_COMMISSION, study=study, balance_amount=-3 * settings.INT_RATIO, vat_rate=21)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_PATIENT_PAYCHECK, study=study, balance_amount=-1 * settings.INT_RATIO, vat_rate=21)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE, study=study, balance_amount=-0.02 * settings.INT_RATIO, vat_rate=21)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_POST_OFFICE_FEE, study=study, balance_amount=-5 * settings.INT_RATIO, vat_rate=21)

        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_TOPUP, study=study, balance_amount=6 * settings.INT_RATIO, vat_rate=21)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_COMMISSION, study=study, balance_amount=-3 * settings.INT_RATIO, vat_rate=21)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_PATIENT_PAYCHECK, study=study, balance_amount=-1 * settings.INT_RATIO, vat_rate=21)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE, study=study, balance_amount=-2 * settings.INT_RATIO, vat_rate=21)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_POST_OFFICE_FEE, study=study, balance_amount=-5 * settings.INT_RATIO, vat_rate=21)

        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_TOPUP, study=study, balance_amount=6 * settings.INT_RATIO, vat_rate=0)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_COMMISSION, study=study, balance_amount=-3 * settings.INT_RATIO, vat_rate=0)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_PATIENT_PAYCHECK, study=study, balance_amount=-1 * settings.INT_RATIO, vat_rate=0)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE, study=study, balance_amount=-2 * settings.INT_RATIO, vat_rate=0)
        baker.make('credit.CreditBalance', balance_type=credit_const.CREDIT_BALANCE_POST_OFFICE_FEE, study=study, balance_amount=-5 * settings.INT_RATIO, vat_rate=0)

        qs = CreditBalance.objects.filter(study__company=study.company).for_invoice()
        data = utils.generate_invoice_data(qs)
        exp_data = [
            {
                'total': 2,
                'balance_type': credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE,
                'study__number': 'test123',
                'vat_rate': 0,
            },
            {
                'total': 2.02,
                'balance_type': credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE,
                'study__number': 'test123',
                'vat_rate': 21,
            },
            {
                'total': 3,
                'balance_type': credit_const.CREDIT_BALANCE_COMMISSION,
                'study__number': 'test123',
                'vat_rate': 0,
            },
            {
                'total': 5,
                'balance_type': credit_const.CREDIT_BALANCE_POST_OFFICE_FEE,
                'study__number': 'test123',
                'vat_rate': 0,
            },
            {
                'total': 6,
                'balance_type': credit_const.CREDIT_BALANCE_COMMISSION,
                'study__number': 'test123',
                'vat_rate': 21,
            },
            {
                'total': 10,
                'balance_type': credit_const.CREDIT_BALANCE_POST_OFFICE_FEE,
                'study__number': 'test123',
                'vat_rate': 21,
            },
        ]
        self.assertEqual(exp_data, data)

    def test_transform_payment_data_to_fakturoid(self):
        data = [
            {
                'total': 2.02,
                'balance_type': credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE,
                'study__number': 'test123',
                'vat_rate': 0,
            },
            {
                'total': 3,
                'balance_type': credit_const.CREDIT_BALANCE_COMMISSION,
                'study__number': 'test123',
                'vat_rate': 0,
            },
            {
                'total': 4,
                'balance_type': credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE,
                'study__number': 'test123',
                'vat_rate': 21,
            },
            {
                'total': 5,
                'balance_type': credit_const.CREDIT_BALANCE_POST_OFFICE_FEE,
                'study__number': 'test123',
                'vat_rate': 0,
            },
            {
                'total': 6,
                'balance_type': credit_const.CREDIT_BALANCE_COMMISSION,
                'study__number': 'test123',
                'vat_rate': 21,
            },
            {
                'total': 10,
                'balance_type': credit_const.CREDIT_BALANCE_POST_OFFICE_FEE,
                'study__number': 'test123',
                'vat_rate': 21,
            },
        ]
        result = utils.transform_payment_data_to_fakturoid(data)
        exp_data = [
            {
                'quantity': 1,
                'name': 'Poplatky za bankovní převod test123',
                'unit_name': 'ks',
                'unit_price_with_vat': 2.02,  # cena bez DPH
                'vat_rate': 0,
            },
            {
                'quantity': 1,
                'name': 'Provize test123',
                'unit_name': 'ks',
                'unit_price_with_vat': 3,  # cena bez DPH
                'vat_rate': 0,
            },
            {
                'quantity': 1,
                'name': 'Poplatky za bankovní převod test123',
                'unit_name': 'ks',
                'unit_price_with_vat': 4,  # cena bez DPH
                'vat_rate': 21,
            },
            {
                'quantity': 1,
                'name': 'Poplatky za poštovní poukázky test123',
                'unit_name': 'ks',
                'unit_price_with_vat': 5,  # cena bez DPH
                'vat_rate': 0,
            },
            {
                'quantity': 1,
                'name': 'Provize test123',
                'unit_name': 'ks',
                'unit_price_with_vat': 6,  # cena bez DPH
                'vat_rate': 21,
            },
            {
                'quantity': 1,
                'name': 'Poplatky za poštovní poukázky test123',
                'unit_name': 'ks',
                'unit_price_with_vat': 10,  # cena bez DPH
                'vat_rate': 21,
            },
        ]
        self.assertEqual(exp_data, result)
