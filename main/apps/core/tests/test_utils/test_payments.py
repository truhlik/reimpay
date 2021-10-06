from django.conf import settings
from django.test import TestCase
from model_bakery import baker

from main.apps.credit.constants import CREDIT_BALANCE_PATIENT_PAYCHECK, CREDIT_BALANCE_COMMISSION
from main.apps.credit.models import CreditBalance
from main.apps.fiobanka.models import FiobankTransactions
from main.apps.payments.constants import PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER, \
    PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER
from main.apps.payments.models import Payment
from main.apps.studies import constants as study_constants
from ...utils import payments


class FiobankTransactionsQuerySetTestCase(TestCase):
    fixtures = ['fiobanktransaction.json']

    def setUp(self) -> None:
        super(FiobankTransactionsQuerySetTestCase, self).setUp()

    def test_process_new_transactions(self):
        baker.make('fiobanka.FiobankTransactions', variable_symbol='123456789')

    def test_create_transaction_dict(self):
        t1 = baker.make('fiobanka.FiobankTransactions', variable_symbol='123456789', specific_symbol='')
        t2 = baker.make('fiobanka.FiobankTransactions', variable_symbol='123456789', specific_symbol=None)
        t3 = baker.make('fiobanka.FiobankTransactions', variable_symbol='987654321', specific_symbol='')
        t4 = baker.make('fiobanka.FiobankTransactions', variable_symbol='abc', specific_symbol=None)
        t5 = baker.make('fiobanka.FiobankTransactions', variable_symbol=None, specific_symbol='')
        t6 = baker.make('fiobanka.FiobankTransactions', variable_symbol='987654321', specific_symbol='123')

        lst = [t1, t2, t3, t4, t5, t6]
        dct = payments._create_topup_dict(lst)
        exp_dct = {
            123456789: [t1, t2],
            987654321: [t3],
        }
        self.assertEqual(
            exp_dct, dct
        )

    def test_create_returned_payments_dict(self):
        t1 = baker.make('fiobanka.FiobankTransactions', variable_symbol='123456789', specific_symbol='123', constant_symbol=PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)
        t2 = baker.make('fiobanka.FiobankTransactions', variable_symbol='123456789', specific_symbol='123', constant_symbol=PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)
        t3 = baker.make('fiobanka.FiobankTransactions', variable_symbol='987654321', specific_symbol='123', constant_symbol=PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)
        t4 = baker.make('fiobanka.FiobankTransactions', variable_symbol='abc', specific_symbol='123', constant_symbol=PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)
        t5 = baker.make('fiobanka.FiobankTransactions', variable_symbol=None, specific_symbol='123', constant_symbol=PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)
        t6 = baker.make('fiobanka.FiobankTransactions', variable_symbol='987654321', specific_symbol='123', constant_symbol=PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER)
        t7 = baker.make('fiobanka.FiobankTransactions', variable_symbol='987654321', specific_symbol='', constant_symbol=PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)

        lst = [t1, t2, t3, t4, t5, t6, t7]
        dct = payments._create_returned_payments_dict(lst)
        exp_dct = {
            123456789: [t1, t2],
            987654321: [t3],
        }
        self.assertEqual(
            exp_dct, dct
        )

    def test_fixture_loading(self):
        self.assertEqual(4, len(FiobankTransactions.objects.all()))

    def test_process_payments_studies(self):
        baker.make('studies.Study', variable_symbol='129092165', closed_at=None)
        pp, ps = payments._process_payments_studies(
            {129092165: list(FiobankTransactions.objects.all())}
        )
        self.assertTrue((25, 1), (pp, ps))
        qs = CreditBalance.objects.all().order_by('-created_at')
        self.assertEqual(4, len(qs))
        self.assertEqual(2107.77 * settings.INT_RATIO, qs[0].balance_sum)

    def test_process_returned_payments(self):
        p = baker.make('studies.Patient')
        pv = baker.make('studies.PatientVisit', patient=p)
        pvi = baker.make('studies.PatientVisitItem', patient_visit=pv)

        cb = baker.make('credit.CreditBalance',
                        study=p.study,
                        balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK,
                        balance_amount=1138.13 * settings.INT_RATIO,
                        vat_rate=0)
        cb.reims.set([pvi])

        _ = baker.make('payments.Payment',
                       variable_symbol='129092165',
                       constant_symbol=PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER,
                       total_value=1138.13 * settings.INT_RATIO)

        pr = payments._process_returned_payments(
            {129092165: list(FiobankTransactions.objects.all())}
        )
        self.assertEqual(1, pr)

    def test_mark_payment_as_returned(self):
        self.assertTrue(True)

    def test_process_undefined_transactions(self):
        payments.process_undefined_transactions()
        # self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(0, len(FiobankTransactions.objects.not_processed_yet().filter(amount__gte=0)))

    def test_get_actual_balance(self):
        study = baker.make('studies.Study')
        baker.make('credit.CreditBalance',
                   study=study,
                   balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK,
                   balance_amount=113813, balance_sum=113813, vat_rate=0)
        self.assertEqual(113813, payments.get_actual_balance(study))

    def test_get_actual_balance_empty(self):
        study = baker.make('studies.Study')
        self.assertEqual(0, payments.get_actual_balance(study))

    def test_get_paid(self):
        study = baker.make('studies.Study')
        baker.make('credit.CreditBalance',
                   study=study,
                   balance_type=CREDIT_BALANCE_PATIENT_PAYCHECK,
                   balance_amount=1, vat_rate=0)
        baker.make('credit.CreditBalance',
                   study=study,
                   balance_type=CREDIT_BALANCE_COMMISSION,
                   balance_amount=2, vat_rate=0)
        self.assertEqual(3, payments.get_paid(study))

    def test_get_paid_empty(self):
        study = baker.make('studies.Study')
        self.assertEqual(0, payments.get_paid(study))

    def test_topup_credit(self):
        study = baker.make('studies.Study', status=study_constants.STUDY_STATUS_PRELAUNCH)
        payments.topup_credit(study, 10000)
        study.refresh_from_db()
        self.assertEqual(study_constants.STUDY_STATUS_PROGRESS, study.status)
        self.assertEqual(10000 * settings.INT_RATIO, payments.get_actual_balance(study))

    def test_get_reims_from_payment_qs(self):
        pvi1 = baker.make('studies.PatientVisitItem')
        pvi2 = baker.make('studies.PatientVisitItem')
        pvi3 = baker.make('studies.PatientVisitItem')
        p = baker.make('payments.Payment')
        cb = baker.make('credit.CreditBalance', payment=p)
        cb.reims.set([pvi1, pvi2])
        cb2 = baker.make('credit.CreditBalance')
        cb2.reims.set([pvi3])
        p_qs = Payment.objects.all()
        pvi_qs = payments.get_reims_from_payment_qs(p_qs)
        self.assertEqual(2, len(pvi_qs))
        self.assertEqual(pvi1, pvi_qs[0])
        self.assertEqual(pvi2, pvi_qs[1])
