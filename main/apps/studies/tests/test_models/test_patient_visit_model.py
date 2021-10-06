from django.test import TestCase

from model_bakery import baker

from main.apps.users import constants as user_constants

from ... import constants


class PatientVisitModelTestCase(TestCase):

    def setUp(self) -> None:
        super(PatientVisitModelTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.study1 = baker.make('studies.Study', company=self.c1, status=constants.STUDY_STATUS_BILLING)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        self.site1 = baker.make('studies.Site', study=self.study1)
        self.patient = baker.make('studies.Patient', arm=self.arm1, site=self.site1, study=self.study1)
        self.visit1 = baker.make('studies.Visit', study=self.study1, arm=self.arm1)
        self.study_item1 = baker.make('studies.StudyItem', study=self.study1)
        self.visit_item = baker.make('studies.VisitItem', study_item=self.study_item1, visit=self.visit1, study=self.study1)
        self.obj1 = baker.make('studies.PatientVisit', patient=self.patient, visit=self.visit1, study=self.study1)
        # self.obj1.visit_items.set([self.visit_item])

    def test_is_owner_admin_associated_with_this_study(self):
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.assertTrue(self.obj1.is_owner(user))

    def test_is_owner_cra_associated_with_this_study(self):
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=self.c1)
        self.site1.cra = user
        self.site1.save()
        self.assertTrue(self.obj1.is_owner(user))

    def test_is_owner_admin_from_other_company(self):
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c2)
        self.assertFalse(self.obj1.is_owner(user))

