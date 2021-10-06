from django.test import TestCase

from model_bakery import baker

from main.apps.studies.models import Visit
from main.apps.studies import utils
from main.apps.users import constants as user_constants

from ... import constants


class VisitModelTestCase(TestCase):

    def setUp(self) -> None:
        super(VisitModelTestCase, self).setUp()

    def test_is_owner_admin_associated_with_this_study(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        obj = baker.make('studies.Visit', study=study1, arm=arm)
        self.assertTrue(obj.is_owner(user))

    def test_is_owner_cra_associated_with_this_study(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        baker.make('studies.Site', cra=user, study=study1)
        arm = baker.make('studies.Arm', study=study1)
        obj = baker.make('studies.Visit', study=study1, arm=arm)
        self.assertTrue(obj.is_owner(user))

    def test_is_owner_admin_from_ther_company(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c2)
        study1 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        obj = baker.make('studies.Visit', study=study1, arm=arm)
        self.assertFalse(obj.is_owner(user))

    def test_custom_delete_billing(self):
        c = baker.make('companies.Company')
        study2 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_BILLING)
        arm = baker.make('studies.Arm', study=study2)
        obj2 = baker.make('studies.Visit', study=study2, arm=arm)
        obj2.custom_delete()
        obj2.refresh_from_db()
        self.assertTrue(obj2.deleted)

    def test_custom_delete_prelaunch(self):
        c = baker.make('companies.Company')
        study2 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_DRAFT)
        arm = baker.make('studies.Arm', study=study2)
        obj2 = baker.make('studies.Visit', study=study2, arm=arm)
        obj2.custom_delete()
        self.assertEqual(0, Visit.objects.all().count())

    def test_order_was_changed_created_item(self):
        c = baker.make('companies.Company')
        study2 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_PRELAUNCH)
        arm = baker.make('studies.Arm', study=study2)
        utils.create_visits(study2, arm)
        visit1 = Visit(order=1, study=study2, arm=arm, title='test', number=1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit1.save()
        visit_new = Visit(order=1, study=study2, arm=arm, title='test', number=1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit_new.save()
        visit1.refresh_from_db()
        self.assertEqual(1, visit_new.order)
        self.assertEqual(2, visit1.order)

    def test_get_order(self):
        c = baker.make('companies.Company')
        study2 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_PRELAUNCH)
        arm = baker.make('studies.Arm', study=study2)
        v = baker.prepare('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        self.assertEqual(1, v._get_order())

    def test_get_order_second(self):
        c = baker.make('companies.Company')
        study2 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_PRELAUNCH)
        arm = baker.make('studies.Arm', study=study2)
        _ = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        v2 = baker.prepare('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        self.assertEqual(2, v2._get_order())

    def test_get_order_other_arm(self):
        c = baker.make('companies.Company')
        study2 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_PRELAUNCH)
        arm = baker.make('studies.Arm', study=study2)
        arm2 = baker.make('studies.Arm', study=study2)
        _ = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        v2 = baker.prepare('studies.Visit', arm=arm2, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        self.assertEqual(1, v2._get_order())

    def test_get_order_other_arm_save(self):
        c = baker.make('companies.Company')
        study2 = baker.make('studies.Study', company=c, status=constants.STUDY_STATUS_PRELAUNCH)
        arm = baker.make('studies.Arm', study=study2)
        arm2 = baker.make('studies.Arm', study=study2)
        _ = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        v2 = baker.make('studies.Visit', arm=arm2, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        self.assertEqual(1, v2.order)

    def test_save_number_unscheduled(self):
        arm = baker.make('studies.Arm', max_unscheduled=0)
        visit = baker.prepare('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_UNSCHEDULED, number=3, arm=arm, study=arm.study)
        visit.save()
        arm.refresh_from_db()
        self.assertEqual(3, arm.max_unscheduled)
