from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from main.apps.users import constants as user_constatnts

from ..models import Payment
from .. import utils
from .. import constants
from ...studies.models import Patient


class CreditBalanceQuerySetTestCase(TestCase):

    def setUp(self) -> None:
        super(CreditBalanceQuerySetTestCase, self).setUp()

    def test_paychecks(self):
        p1 = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_COMMISSION)
        p2 = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_FEE_POST_OFFICE)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_TOPDOWN)
        qs = Payment.objects.paychecks()
        self.assertEqual(2, len(qs))
        self.assertIn(p1, qs)
        self.assertIn(p2, qs)

    def test_fee(self):
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)
        p1 = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_COMMISSION)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE)
        p2 = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_FEE_POST_OFFICE)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_TOPDOWN)
        qs = Payment.objects.fee()
        self.assertEqual(2, len(qs))
        self.assertIn(p1, qs)
        self.assertIn(p2, qs)

    def test_commissions(self):
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_BANK_TRANSFER)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_FEE_BANK_TRANSFER)
        p1 = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_COMMISSION)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_FEE_POST_OFFICE)
        _ = baker.make(Payment, constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_TOPDOWN)
        qs = Payment.objects.commissions()
        self.assertEqual(1, len(qs))
        self.assertIn(p1, qs)

    def test_not_sent(self):
        p1 = baker.make(Payment, sent_on=None)
        _ = baker.make(Payment, sent_on=timezone.now())
        qs = Payment.objects.not_sent()
        self.assertEqual(1, len(qs))
        self.assertIn(p1, qs)

    def test_for_patient(self):
        patient = baker.make('studies.Patient')
        pv = baker.make('studies.PatientVisit', patient=patient)
        pvi1 = baker.make('studies.PatientVisitItem', patient_visit=pv, visit_item__study_item__price=100)
        pvi2 = baker.make('studies.PatientVisitItem', patient_visit=pv, visit_item__study_item__price=200)
        payment = baker.make('payments.Payment')
        cb = baker.make('credit.CreditBalance', payment=payment)
        _ = baker.make('credit.CreditBalance', payment=payment)
        cb.reims.set([pvi1, pvi2])

        qs = Payment.objects.for_patient(patient)
        self.assertEqual(1, len(qs))
        self.assertEqual(payment, qs[0])

    def test_delivered(self):
        t40 = timezone.now() - timezone.timedelta(days=40)
        t20 = timezone.now() - timezone.timedelta(days=20)
        t10 = timezone.now() - timezone.timedelta(days=10)
        p1 = baker.make('payments.Payment', sent_on=None, returned_on=None, resent_on=None)
        p2 = baker.make('payments.Payment', sent_on=t40, returned_on=None, resent_on=None)  # delivered
        p3 = baker.make('payments.Payment', sent_on=t40, returned_on=t20, resent_on=None)
        p4 = baker.make('payments.Payment', sent_on=t40, returned_on=t20, resent_on=t10)  # delivered
        p5 = baker.make('payments.Payment', sent_on=t20, returned_on=None, resent_on=None)
        p6 = baker.make('payments.Payment', sent_on=t20, returned_on=t10, resent_on=None)
        p7 = baker.make('payments.Payment', sent_on=t10, returned_on=None, resent_on=None)
        qs = Payment.objects.delivered()
        self.assertEqual(2, len(qs))
        self.assertEqual([p2.id, p4.id], list(qs.order_by('id').values_list('id', flat=True)))

    def test_not_delivered(self):
        t40 = timezone.now() - timezone.timedelta(days=40)
        t20 = timezone.now() - timezone.timedelta(days=20)
        t10 = timezone.now() - timezone.timedelta(days=10)
        p1 = baker.make('payments.Payment', sent_on=None, returned_on=None, resent_on=None)  # not delivered
        p2 = baker.make('payments.Payment', sent_on=t40, returned_on=None, resent_on=None)
        p3 = baker.make('payments.Payment', sent_on=t40, returned_on=t20, resent_on=None)  # not delivered
        p4 = baker.make('payments.Payment', sent_on=t40, returned_on=t20, resent_on=t10)
        p5 = baker.make('payments.Payment', sent_on=t20, returned_on=None, resent_on=None)  # not delivered
        p6 = baker.make('payments.Payment', sent_on=t20, returned_on=t10, resent_on=None)  # not delivered
        p7 = baker.make('payments.Payment', sent_on=t10, returned_on=None, resent_on=None)  # not delivered
        qs = Payment.objects.not_delivered()
        self.assertEqual(5, len(qs))
        self.assertEqual([p1.id, p3.id, p5.id, p6.id, p7.id], list(qs.order_by('id').values_list('id', flat=True)))
