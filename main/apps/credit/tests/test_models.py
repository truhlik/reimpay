from django.test import TestCase
from model_bakery import baker

from main.apps.credit.models import CreditBalance


class CreditBalanceModelTestCase(TestCase):

    def setUp(self) -> None:
        super(CreditBalanceModelTestCase, self).setUp()

    def test_save_without_balance_amount(self):
        study = baker.make('studies.Study')
        credit = baker.prepare('credit.CreditBalance', item_amount=100, balance_amount=None, vat_rate=21, study=study)
        credit.save()
        self.assertEqual(121, credit.balance_amount)

    def test_save_without_vat_amount(self):
        study = baker.make('studies.Study')
        credit = baker.prepare('credit.CreditBalance', item_amount=100, vat_amount=None, vat_rate=21, study=study)
        credit.save()
        self.assertEqual(21, credit.vat_amount)

    def test_create_credit_balance(self):
        study = baker.make('studies.Study', commission=10)
        si = baker.make('studies.StudyItem', price=100, study=study)
        vi = baker.make('studies.VisitItem', study_item=si, study=study)
        pv = baker.make('studies.PatientVisit', study=study)
        pvi = baker.prepare('studies.PatientVisitItem', patient_visit=pv, visit_item=vi)
        pvi.approved = True
        pvi.save()
        qs = CreditBalance.objects.all()
        self.assertEqual(1, len(qs))
