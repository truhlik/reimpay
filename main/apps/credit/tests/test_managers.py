from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from main.apps.users import constants as user_constatnts

from ..models import CreditBalance
from .. import utils
from .. import constants
from ...studies.models import Patient


class CreditBalanceQuerySetTestCase(TestCase):

    def setUp(self) -> None:
        super(CreditBalanceQuerySetTestCase, self).setUp()

    def test_paychecks(self):
        cb = baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_TOPUP)
        baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_COMMISSION)
        qs = CreditBalance.objects.paychecks()
        self.assertEqual(1, len(qs))
        self.assertEqual(cb, qs[0])

    def test_topups(self):
        baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        cb = baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_TOPUP)
        baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_COMMISSION)
        qs = CreditBalance.objects.topups()
        self.assertEqual(1, len(qs))
        self.assertEqual(cb, qs[0])

    def test_owner_admin(self):
        c1 = baker.make('companies.Company')

        user_admin = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=c1)

        study1 = baker.make('studies.Study', company=c1)
        study2 = baker.make('studies.Study', company=c1)

        cb1 = baker.make('credit.CreditBalance', study=study1)
        cb2 = baker.make('credit.CreditBalance', study=study2)
        _ = baker.make('credit.CreditBalance')

        qs = CreditBalance.objects.owner(user_admin)
        self.assertEqual(2, len(qs))
        self.assertIn(cb1, qs)
        self.assertIn(cb2, qs)

    def test_owner_cra(self):
        c1 = baker.make('companies.Company')

        user_cra = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=c1)

        study1 = baker.make('studies.Study', company=c1)
        baker.make('studies.Site', cra=user_cra, study=study1)
        study2 = baker.make('studies.Study', company=c1)

        cb1 = baker.make('credit.CreditBalance', study=study1)
        cb2 = baker.make('credit.CreditBalance', study=study2)
        _ = baker.make('credit.CreditBalance')

        qs = CreditBalance.objects.owner(user_cra)
        self.assertEqual(1, len(qs))
        self.assertIn(cb1, qs)

    def test_for_patient(self):
        patient = baker.make('studies.Patient', study__variable_symbol=123456, payment_info='patinet_bank_acount')
        pv = baker.make('studies.PatientVisit', patient=patient)
        pvi1 = baker.make('studies.PatientVisitItem', patient_visit=pv, visit_item__study_item__price=100)
        pvi2 = baker.make('studies.PatientVisitItem', patient_visit=pv, visit_item__study_item__price=200)
        cb = baker.make('credit.CreditBalance', payment=None, balance_amount=-300, vat_rate=0)
        _ = baker.make('credit.CreditBalance', payment=None, balance_amount=-300, vat_rate=0)
        cb.reims.set([pvi1, pvi2])

        qs = CreditBalance.objects.for_patient(patient)
        self.assertEqual(1, len(qs))
        self.assertEqual(cb, qs[0])

    def test_not_processed(self):
        payment = baker.make('payments.Payment')
        cb = baker.make('credit.CreditBalance', payment=None, balance_amount=-300, vat_rate=0)
        _ = baker.make('credit.CreditBalance', payment=payment, balance_amount=-300, vat_rate=0)

        qs = CreditBalance.objects.not_processed()
        self.assertEqual(1, len(qs))
        self.assertEqual(cb, qs[0])

    def test_for_patients(self):
        p2 = baker.make('studies.Patient')
        p1 = baker.make('studies.Patient')
        pv1 = baker.make('studies.PatientVisit', patient=p1)
        pv2 = baker.make('studies.PatientVisit', patient=p2)
        pvi1 = baker.make('studies.PatientVisitItem', patient_visit=pv1, visit_item__study_item__price=100)
        pvi2 = baker.make('studies.PatientVisitItem', patient_visit=pv2, visit_item__study_item__price=200)
        cb1 = baker.make('credit.CreditBalance', payment=None, balance_amount=-300, vat_rate=0)
        cb1.reims.set([pvi1])
        cb2 = baker.make('credit.CreditBalance', payment=None, balance_amount=-300, vat_rate=0)
        cb2.reims.set([pvi2])
        _ = baker.make('credit.CreditBalance', payment=None, balance_amount=-300, vat_rate=0)

        p_qs = Patient.objects.filter(id__in=[p1.id, p2.id])
        qs = CreditBalance.objects.for_patients(p_qs)
        self.assertEqual(2, len(qs))
        self.assertEqual([cb1.id, cb2.id], list(qs.order_by('id').values_list('id', flat=True)))

    def test_without_commission(self):
        cb1 = baker.make('credit.CreditBalance', commission=None, vat_rate=0)
        _ = baker.make('credit.CreditBalance', commission=cb1, vat_rate=0)
        qs = CreditBalance.objects.without_commission()
        self.assertEqual(1, len(qs))
        self.assertEqual(cb1, qs[0])

    def test_get_balance_amount_sum(self):
        _ = baker.make('credit.CreditBalance', balance_amount=-300)
        _ = baker.make('credit.CreditBalance', balance_amount=100)
        self.assertEqual(-200, CreditBalance.objects.get_balance_amount_sum())

    def test_output(self):
        baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        cb = baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_TOPUP)
        baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_COMMISSION)
        baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_POST_OFFICE_FEE)
        baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_BANK_TRANSFER_FEE)
        qs = CreditBalance.objects.output()
        self.assertEqual(4, len(qs))
        self.assertNotIn(cb, qs)

    def test_for_invoice(self):
        _ = baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_TOPUP)
        p1 = baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_COMMISSION)
        _ = baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        p2 = baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_BANK_TRANSFER_FEE)
        p3 = baker.make(CreditBalance, balance_type=constants.CREDIT_BALANCE_POST_OFFICE_FEE)
        qs = CreditBalance.objects.for_invoice().order_by('id')
        self.assertEqual(3, len(qs))
        self.assertEqual(p1, qs[0])
        self.assertEqual(p2, qs[1])
        self.assertEqual(p3, qs[2])

    def test_not_invoiced(self):
        _ = baker.make(CreditBalance, invoiced_on=timezone.now())
        p1 = baker.make(CreditBalance, invoiced_on=None)
        qs = CreditBalance.objects.not_invoiced().order_by('id')
        self.assertEqual(1, len(qs))
        self.assertEqual(p1, qs[0])
