from django.test import TestCase

from model_bakery import baker

from main.apps.users import constants as user_constants

from ... import constants
from ...models.patients import PatientPaymentData


class PatientModelTestCase(TestCase):

    def setUp(self) -> None:
        super(PatientModelTestCase, self).setUp()

    def test_is_owner_admin_associated_with_this_study(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)
        obj = baker.make('studies.Patient', study=study1, arm=arm, site=site)
        self.assertTrue(obj.is_owner(user))

    def test_is_owner_cra_associated_with_this_study(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1, cra=user)
        obj = baker.make('studies.Patient', study=study1, arm=arm, site=site)
        self.assertTrue(obj.is_owner(user))

    def test_is_owner_admin_from_ther_company(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c2)
        study1 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)
        obj = baker.make('studies.Patient', study=study1, arm=arm, site=site)
        self.assertFalse(obj.is_owner(user))

    def test_should_normalize_payment_data_new_object(self):
        c = baker.make('companies.Company')
        study1 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_DRAFT)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)
        p = baker.prepare('studies.Patient', study=study1, arm=arm, site=site)
        self.assertTrue(p._should_normalize_payment_data())

    def test_should_normalize_payment_data_created(self):
        c = baker.make('companies.Company')
        study1 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_DRAFT)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)
        p = baker.make('studies.Patient', study=study1, arm=arm, site=site)
        self.assertFalse(p._should_normalize_payment_data())

    def test_should_normalize_payment_data_true(self):
        c = baker.make('companies.Company')
        study1 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_DRAFT)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)
        p = baker.make('studies.Patient', study=study1, arm=arm, site=site)
        p.payment_info = 'test'
        self.assertTrue(p._should_normalize_payment_data())
        p.save()
        self.assertEqual(2, PatientPaymentData.objects.all().count())
        self.assertFalse(p._should_normalize_payment_data())

    def test_payment_data_not_saved(self):
        c = baker.make('companies.Company')
        study1 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_DRAFT)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)
        p = baker.prepare('studies.Patient', study=study1, arm=arm, site=site)
        self.assertIsNone(p._payment_data)

    def test_payment_data_created(self):
        c = baker.make('companies.Company')
        study1 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_DRAFT)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)
        p = baker.make('studies.Patient', study=study1, arm=arm, site=site)
        self.assertIsNotNone(p._payment_data)
