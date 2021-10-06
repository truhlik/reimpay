from django.test import TestCase

from model_bakery import baker

from main.apps.studies.models import VisitItem
from main.apps.users import constants as user_constants

from ... import constants
from ...constants import STUDY_VISIT_TYPE_REGULAR


class VisitItemModelTestCase(TestCase):

    def setUp(self) -> None:
        super(VisitItemModelTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.study1 = baker.make('studies.Study', company=self.c1, status=constants.STUDY_STATUS_BILLING)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        self.visit1 = baker.make('studies.Visit', study=self.study1, arm=self.arm1, visit_type=STUDY_VISIT_TYPE_REGULAR)
        self.study_item1 = baker.make('studies.StudyItem', study=self.study1, price=100)
        self.obj1 = baker.make('studies.VisitItem', study_item=self.study_item1, visit=self.visit1, study=self.study1)

    def test_is_owner_admin_associated_with_this_study(self):
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.assertTrue(self.obj1.is_owner(user))

    def test_is_owner_cra_associated_with_this_study(self):
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=self.c1)
        self.assertFalse(self.obj1.is_owner(user))

    def test_is_owner_admin_from_other_company(self):
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c2)
        self.assertFalse(self.obj1.is_owner(user))

    def test_custom_delete_billing(self):
        self.study1.status = constants.STUDY_STATUS_PROGRESS
        self.obj1.custom_delete()
        self.obj1.refresh_from_db()
        self.assertTrue(self.obj1.deleted)

    def test_custom_delete_prelaunch(self):
        self.study1.status = constants.STUDY_STATUS_DRAFT
        self.obj1.custom_delete()
        self.assertEqual(0, VisitItem.objects.all().count())

    def test_get_visit_item_cost(self):
        self.assertEqual(100, self.arm1.d_visit_items_cost)
