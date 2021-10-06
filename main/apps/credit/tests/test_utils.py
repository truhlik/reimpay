from django.conf import settings
from django.http import HttpResponse
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from ..models import CreditBalance
from .. import utils, functions
from .. import constants
from ...studies.models import PatientVisitItem


class UtilsTestCase(TestCase):

    def setUp(self) -> None:
        super(UtilsTestCase, self).setUp()

    def test_add_credit_to_study(self):
        study = baker.make('studies.Study')
        utils.add_credit_to_study(study, 1)
        qs = CreditBalance.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(settings.INT_RATIO, qs[0].balance_sum)

    def test_get_patient_from_credit(self):
        p = baker.make('studies.Patient')
        pv = baker.make('studies.PatientVisit', patient=p)
        pvi = baker.make('studies.PatientVisitItem', patient_visit=pv)

        payment = baker.make(CreditBalance, balance_amount=100, balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        payment.reims.set([pvi])
        patient = utils.get_patient_from_credit(payment)

        self.assertEqual(p, patient)

    def test_create_commission_balance(self):
        study = baker.make('studies.Study', commission=3)
        _ = baker.make('credit.CreditBalance', balance_amount=-300, balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        _ = baker.make('credit.CreditBalance', balance_amount=100, balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        utils._create_commission_balance(study, CreditBalance.objects.all())
        qs = CreditBalance.objects.commissions()
        self.assertEqual(1, len(qs))
        obj = qs[0]
        self.assertEqual(-6, obj.balance_amount)
        self.assertEqual(constants.CREDIT_BALANCE_COMMISSION, obj.balance_type)

    def test_create_paycheck_balance(self):
        study = baker.make('studies.Study', commission=10)
        si = baker.make('studies.StudyItem', price=100, study=study)
        vi = baker.make('studies.VisitItem', study_item=si, study=study)
        pv = baker.make('studies.PatientVisit', study=study)
        pvi = baker.make('studies.PatientVisitItem', patient_visit=pv, visit_item=vi)
        utils._create_paycheck_balance(pvi)
        qs = CreditBalance.objects.paychecks()
        self.assertEqual(1, len(qs))
        obj = qs[0]
        self.assertEqual(-100 * settings.INT_RATIO, obj.balance_amount)
        self.assertEqual(constants.CREDIT_BALANCE_PATIENT_PAYCHECK, obj.balance_type)

    def test_generate_commission_for_study(self):
        study = baker.make('studies.Study', commission=10)
        _ = baker.make('credit.CreditBalance', study=study, balance_amount=-300, balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        _ = baker.make('credit.CreditBalance', study=study, balance_amount=-100, balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        utils.generate_commission_for_study(study)
        qs = CreditBalance.objects.commissions()
        self.assertEqual(1, len(qs))
        obj = qs[0]
        self.assertEqual(-40, obj.balance_amount)
        self.assertEqual(constants.CREDIT_BALANCE_COMMISSION, obj.balance_type)

    def test_get_credit_balance(self):
        study = baker.make('studies.Study', commission=10)
        _ = baker.make('credit.CreditBalance', study=study, balance_sum=-300)
        self.assertEqual(-300, functions.get_credit_balance(study))

    def test_get_credit_balance_empty(self):
        study = baker.make('studies.Study', commission=10)
        self.assertEqual(0, functions.get_credit_balance(study))

    def test_get_credit_balance_after_save(self):
        study = baker.make('studies.Study', commission=10)
        _ = baker.make('credit.CreditBalance', study=study, balance_amount=-300)
        self.assertEqual(-300, functions.get_credit_balance(study))

    def test_get_csv_export(self):
        c1 = baker.make('credit.CreditBalance', balance_amount=-1210 * settings.INT_RATIO, vat_rate=21, vat_amount=None, item_amount=None,
                       balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        _ = baker.make('credit.CreditBalance', balance_amount=-2420 * settings.INT_RATIO, vat_rate=21, vat_amount=None, item_amount=None,
                       balance_type=constants.CREDIT_BALANCE_PATIENT_PAYCHECK)
        response = HttpResponse()
        qs = CreditBalance.objects.all()
        csv = utils.get_csv_export(response, qs)
        data = response.content.decode().splitlines()
        self.assertEqual(3, len(data))  # ocekavam 3 radky
        self.assertEqual(5, len(data[1].split(',')))  # ocekavam 5 radku

        date = timezone.now().date().strftime('%Y-%m-%d')
        self.assertEqual(
            '{},-1210.0,-1000.0,-210.0,{}'.format(date, c1.get_balance_type_display()),
            data[1]
        )
