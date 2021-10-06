from constance import config
from django.conf import settings
from django.utils import timezone

from django.test import TestCase
from model_bakery import baker

from .. import utils
from .. import constants
from ..models import PaycheckGeneration, Payment
from ...core.constants import PAYMENT_TYPE_POST_OFFICE, PAYMENT_TYPE_BANK_TRANSFER
from ...credit.constants import CREDIT_BALANCE_PATIENT_PAYCHECK, CREDIT_BALANCE_BANK_TRANSFER_FEE, \
    CREDIT_BALANCE_COMMISSION
from ...credit.models import CreditBalance
from ...studies.constants import STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_WAITING, \
    STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_SENT, STUDY_STATUS_PRELAUNCH


class UtilsTestCase(TestCase):

    def setUp(self) -> None:
        super(UtilsTestCase, self).setUp()

    def test_can_generate_paychecks_launched(self):
        study = baker.make('studies.Study', progress_at=timezone.now() - timezone.timedelta(days=10), pay_frequency=1)
        self.assertFalse(utils._can_generate_paychecks(study))

    def test_can_generate_paychecks_launched_before(self):
        study = baker.make('studies.Study', progress_at=timezone.now() - timezone.timedelta(days=40), pay_frequency=1)
        self.assertTrue(utils._can_generate_paychecks(study))

    def test_can_generate_paychecks_already_generated(self):
        study = baker.make('studies.Study', progress_at=timezone.now() - timezone.timedelta(days=40), pay_frequency=1)
        PaycheckGeneration.objects.create(study=study)
        self.assertFalse(utils._can_generate_paychecks(study))

    def test_get_days_from_pay_frequency(self):
        date = timezone.datetime(year=2020, month=3, day=3)
        self.assertEqual(91, utils.get_days_from_pay_frequency(3, date))

    # def test_generate_bank_transfer_paycheck_for_patient(self):
    #     config.BANK_ACCOUNT_CREDIT = 'test'
    #     patient = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_BANK_TRANSFER, study__variable_symbol=123456, payment_info='patinet_bank_acount')
    #     pv = baker.make('studies.PatientVisit', patient=patient)
    #     pvi1 = baker.make('studies.PatientVisitItem', patient_visit=pv, visit_item__study_item__price=100)
    #     pvi2 = baker.make('studies.PatientVisitItem', patient_visit=pv, visit_item__study_item__price=200)
    #     cb = baker.make('credit.CreditBalance', balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK, payment=None, balance_amount=-300)
    #     cb.reims.set([pvi1, pvi2])
    #     self.assertTrue(utils._generate_bank_transfer_paycheck_for_patient(patient))
    #     cb.refresh_from_db()
    #
    #     payment = Payment.objects.all().first()
    #     self.assertEqual(payment, cb.payment)
    #     self.assertEqual(300, payment.total_value)
    #
    # def test_generate_bank_transfer_paycheck_for_patient_without_credit_balance(self):
    #     patient = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_BANK_TRANSFER, study__variable_symbol=123456, payment_info='patinet_bank_acount')
    #     self.assertFalse(utils._generate_bank_transfer_paycheck_for_patient(patient))

    # def test_generate_post_office_paycheck_for_patient(self):
    #     config.BANK_ACCOUNT_CREDIT = 'test'
    #
    #     patient = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_POST_OFFICE, study__variable_symbol=123456, payment_info='patinet_bank_acount')
    #     pv = baker.make('studies.PatientVisit', patient=patient)
    #     pvi1 = baker.make('studies.PatientVisitItem', patient_visit=pv, visit_item__study_item__price=100)
    #     pvi2 = baker.make('studies.PatientVisitItem', patient_visit=pv, visit_item__study_item__price=200)
    #     cb = baker.make('credit.CreditBalance', balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK, payment=None, balance_amount=-300)
    #     _ = baker.make('credit.CreditBalance', payment=None, balance_amount=-300, balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK)
    #     cb.reims.set([pvi1, pvi2])
    #
    #     self.assertTrue(utils._generate_post_office_paycheck_for_patient(patient, patient.study))
    #     cb.refresh_from_db()
    #
    #     payment = Payment.objects.all().first()
    #     self.assertEqual(payment, cb.payment)
    #     self.assertEqual(300, payment.total_value)
    #
    # def test_generate_post_office_paycheck_for_patient_without_credit_balance(self):
    #     patient = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_POST_OFFICE, study__variable_symbol=123456, payment_info='patinet_bank_acount')
    #     self.assertFalse(utils._generate_post_office_paycheck_for_patient(patient, patient.study))

    def test_create_credit_fee_balance(self):
        payment = baker.make('payments.Payment', total_value=100)
        fee_type = PAYMENT_TYPE_BANK_TRANSFER
        utils._create_credit_fee_balance(payment, fee_type)
        qs = CreditBalance.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(-100, qs[0].balance_amount)

    def test_generate_payment_fee(self):
        config.BANK_ACCOUNT_CREDIT = 'credit'
        config.BANK_ACCOUNT_OPERATIONAL = 'operation'

        fee = 100
        study = baker.make('studies.Study', variable_symbol=123456)
        utils._generate_payment_fee(fee, study, constants.PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER, 21)
        qs = Payment.objects.fee()
        self.assertEqual(1, len(qs))
        self.assertEqual(config.BANK_ACCOUNT_CREDIT, qs[0].bank_account_from)
        self.assertEqual(config.BANK_ACCOUNT_OPERATIONAL, qs[0].bank_account_to)
        self.assertEqual(1, CreditBalance.objects.fee().count())

    def test_generate_payments_patients(self):
        config.BANK_ACCOUNT_CREDIT = 'test'
        config.BANK_TRANSFER_FEE = 100
        config.POST_OFFICE_FEE = 200

        study = baker.make('studies.Study', variable_symbol=123456)
        p1 = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_POST_OFFICE, study=study, payment_info='patinet_bank_acount')
        p2 = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_POST_OFFICE, study=study, payment_info='patinet_bank_acount')
        p3 = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_BANK_TRANSFER, study=study, payment_info='patinet_bank_acount')
        p4 = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_BANK_TRANSFER, study=study, payment_info='patinet_bank_acount')

        pvi1 = baker.make('studies.PatientVisitItem', patient_visit__patient=p1, visit_item__study_item__price=100)
        pvi2 = baker.make('studies.PatientVisitItem', patient_visit__patient=p2, visit_item__study_item__price=200)
        pvi3 = baker.make('studies.PatientVisitItem', patient_visit__patient=p3, visit_item__study_item__price=300)
        pvi4 = baker.make('studies.PatientVisitItem', patient_visit__patient=p4, visit_item__study_item__price=400)

        cb1 = baker.make('credit.CreditBalance', balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK, payment=None, balance_amount=-100)
        cb1.reims.set([pvi1])

        cb2 = baker.make('credit.CreditBalance', balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK, payment=None, balance_amount=-200)
        cb2.reims.set([pvi2])

        cb3 = baker.make('credit.CreditBalance', balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK, payment=None, balance_amount=-300)
        cb3.reims.set([pvi3])

        cb4 = baker.make('credit.CreditBalance', balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK, payment=None, balance_amount=-400)
        cb4.reims.set([pvi4])

        utils.generate_payments_for_patients(study)

        cb1.refresh_from_db()
        self.assertIsNotNone(cb1.payment)

        cb2.refresh_from_db()
        self.assertIsNotNone(cb2.payment)

        cb3.refresh_from_db()
        self.assertIsNotNone(cb3.payment)

        cb4.refresh_from_db()
        self.assertIsNotNone(cb4.payment)

        qs = Payment.objects.paychecks()
        self.assertEqual(4, len(qs))

        qs = Payment.objects.fee()
        self.assertEqual(2, len(qs))

        # testuju, že se mi vygeneroval CreditBalance
        self.assertEqual(2, len(CreditBalance.objects.fee()))

    def test_generate_payments_for_patients_with_bank_transfer_with_0_sum(self):
        config.BANK_ACCOUNT_CREDIT = 'test'
        config.BANK_TRANSFER_FEE = 0

        study = baker.make('studies.Study', variable_symbol=123456)
        p1 = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_BANK_TRANSFER, study=study, payment_info='patinet_bank_acount')
        pvi1 = baker.make('studies.PatientVisitItem', patient_visit__patient=p1, visit_item__study_item__price=100)

        cb1 = baker.make('credit.CreditBalance', balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK, payment=None, balance_amount=-100)
        cb1.reims.set([pvi1])

        utils.generate_payments_for_patients(study)

        qs = Payment.objects.paychecks()
        self.assertEqual(1, len(qs))

        qs = Payment.objects.fee()
        self.assertEqual(0, len(qs))

        # testuju, že se mi vygeneroval CreditBalance
        self.assertEqual(0, len(CreditBalance.objects.fee()))

    def test_generate_payments_with_0_sum(self):
        config.BANK_ACCOUNT_CREDIT = 'test'
        config.POST_OFFICE_FEE = 100
        config.BANK_TRANSFER_FEE = 100

        study = baker.make('studies.Study', variable_symbol=123456)

        utils.generate_payments_for_patients(study)

        qs = Payment.objects.paychecks()
        self.assertEqual(0, len(qs))

        qs = Payment.objects.fee()
        self.assertEqual(0, len(qs))

        # testuju, že se mi vygeneroval CreditBalance
        self.assertEqual(0, len(CreditBalance.objects.fee()))

    def test_generate_commission_payment(self):
        config.BANK_ACCOUNT_CREDIT = 'credit'
        config.BANK_ACCOUNT_OPERATIONAL = 'operational'

        study = baker.make('studies.Study', variable_symbol=123456)

        cb1 = baker.make('credit.CreditBalance', study=study, balance_type=CREDIT_BALANCE_COMMISSION, payment=None, balance_amount=-200)
        cb2 = baker.make('credit.CreditBalance', study=study, balance_type=CREDIT_BALANCE_COMMISSION, payment=None, balance_amount=-300)

        utils._generate_commission_payment(study)
        qs = Payment.objects.commissions()

        self.assertEqual(1, len(qs))
        self.assertEqual(500, qs[0].total_value)
        cb1.refresh_from_db()
        self.assertEqual(qs[0], cb1.payment)

    def test_generate_payment_data_for_post_office(self):
        study = baker.make('studies.Study', variable_symbol=123456)
        study2 = baker.make('studies.Study', variable_symbol=98765)
        baker.make('payments.Payment',
                   study=study,
                   total_value=2 * settings.INT_RATIO,
                   bank_account_from='1',
                   bank_account_to='2',
                   variable_symbol=study.variable_symbol,
                   specific_symbol=1,
                   constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE)
        baker.make('payments.Payment',
                   study=study,
                   total_value=3 * settings.INT_RATIO,
                   bank_account_from='1',
                   bank_account_to='2',
                   variable_symbol=study.variable_symbol,
                   specific_symbol=1,
                   constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE)
        baker.make('payments.Payment',
                   study=study2,
                   total_value=3 * settings.INT_RATIO,
                   bank_account_from='1',
                   bank_account_to='2',
                   variable_symbol=study2.variable_symbol,
                   specific_symbol=3,
                   constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE)
        baker.make('payments.Payment',
                   study=study2,
                   total_value=3 * settings.INT_RATIO,
                   bank_account_from='1',
                   bank_account_to='2',
                   variable_symbol=study2.variable_symbol,
                   specific_symbol=3,
                   constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE)
        data, qs = utils.generate_payment_data_for_post_office()
        exp_data = [
            {
                'bank_account_from': '1',
                'bank_account_to': '2',
                'value': 5,
                'variable_symbol': study.variable_symbol,
                'constant_symbol': constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE,
            },
            {
                'bank_account_from': '1',
                'bank_account_to': '2',
                'value': 6,
                'variable_symbol': study2.variable_symbol,
                'constant_symbol': constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE,
            },
        ]
        self.assertEqual(2, len(data))
        self.assertEqual(exp_data, data)

    def test_generate_payment_data_without_post_office(self):
        study = baker.make('studies.Study', variable_symbol=123456)
        study2 = baker.make('studies.Study', variable_symbol=123456)
        baker.make('payments.Payment',
                   study=study,
                   total_value=1 * settings.INT_RATIO,
                   bank_account_from='1',
                   bank_account_to='2',
                   variable_symbol=1,
                   specific_symbol=None,
                   constant_symbol=constants.PAYMENT_TYPE_CONSTANT_FEE_POST_OFFICE)
        baker.make('payments.Payment',
                   study=study,
                   total_value=2 * settings.INT_RATIO,
                   bank_account_from='1',
                   bank_account_to='2',
                   variable_symbol=2,
                   specific_symbol=None,
                   constant_symbol=constants.PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER)
        baker.make('payments.Payment',
                   study=study2,
                   total_value=3 * settings.INT_RATIO,
                   bank_account_from='1',
                   bank_account_to='2',
                   variable_symbol=3,
                   specific_symbol=None,
                   constant_symbol=constants.PAYMENT_TYPE_CONSTANT_COMMISSION)
        baker.make('payments.Payment',
                   study=study2,
                   total_value=4 * settings.INT_RATIO,
                   bank_account_from='1',
                   bank_account_to='2',
                   variable_symbol=4,
                   specific_symbol=None,
                   constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)
        exp_data = [
            {
                'bank_account_from': '1',
                'bank_account_to': '2',
                'value': 1,
                'variable_symbol': 1,
                'specific_symbol': None,
                'constant_symbol': constants.PAYMENT_TYPE_CONSTANT_FEE_POST_OFFICE,
            },
            {
                'bank_account_from': '1',
                'bank_account_to': '2',
                'value': 2,
                'variable_symbol': 2,
                'specific_symbol': None,
                'constant_symbol': constants.PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER,
            },
            {
                'bank_account_from': '1',
                'bank_account_to': '2',
                'value': 3,
                'variable_symbol': 3,
                'specific_symbol': None,
                'constant_symbol': constants.PAYMENT_TYPE_CONSTANT_COMMISSION,
            },
            {
                'bank_account_from': '1',
                'bank_account_to': '2',
                'value': 4,
                'variable_symbol': 4,
                'specific_symbol': None,
                'constant_symbol': constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER,
            },
        ]
        data, qs = utils.generate_payment_data_without_post_office()
        self.assertEqual(4, len(data))
        self.assertEqual(exp_data, data)

    def test_mark_payments_as_sent(self):
        pvi1 = baker.make('studies.PatientVisitItem')
        pvi2 = baker.make('studies.PatientVisitItem')
        pvi3 = baker.make('studies.PatientVisitItem')
        p = baker.make('payments.Payment')
        cb = baker.make('credit.CreditBalance', payment=p)
        cb.reims.set([pvi1, pvi2])
        cb2 = baker.make('credit.CreditBalance')
        cb2.reims.set([pvi3])
        p_qs = Payment.objects.all()
        utils.mark_payments_as_sent(p_qs)
        pvi1.refresh_from_db()
        pvi2.refresh_from_db()
        pvi3.refresh_from_db()
        self.assertEqual(pvi1.payment_status, STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_SENT)
        self.assertEqual(pvi2.payment_status, STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_SENT)
        self.assertEqual(pvi3.payment_status, STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_WAITING)

    def test_get_bank_account_for_patient_with_po(self):
        config.POST_OFFICE_BANK_ACCOUNT = '123456789/0800'
        patient = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_POST_OFFICE)
        self.assertEqual('123456789/0800', utils.get_bank_account_for_patient(patient))

    def test_get_bank_account_for_patient_with_bt(self):
        patient = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_BANK_TRANSFER, payment_info='987654321/0800')
        self.assertEqual('987654321/0800', utils.get_bank_account_for_patient(patient))

    def test_get_const_symbol_for_patient_with_po(self):
        config.POST_OFFICE_BANK_ACCOUNT = '123456789/0800'
        patient = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_POST_OFFICE)
        self.assertEqual(constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE,
                         utils.get_const_symbol_for_patient_paycheck_payment(patient))

    def test_get_const_symbol_for_patient_with_bt(self):
        patient = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_BANK_TRANSFER, payment_info='987654321/0800')
        self.assertEqual(constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER,
                         utils.get_const_symbol_for_patient_paycheck_payment(patient))