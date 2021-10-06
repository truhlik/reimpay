from django.test import TestCase

from model_bakery import baker

from main.apps.users import constants as user_constants

from ... import constants


class StudyItemModelTestCase(TestCase):

    def setUp(self) -> None:
        super(StudyItemModelTestCase, self).setUp()

    def test_is_owner_admin_associated_with_this_study(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        self.assertTrue(study_item1.is_owner(user))

    def test_is_owner_cra_associated_with_this_study(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        baker.make('studies.Site', cra=user, study=study1)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        self.assertTrue(study_item1.is_owner(user))

    def test_is_owner_admin_from_ther_company(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c2)
        study1 = baker.make('studies.Study', company=c)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        self.assertFalse(study_item1.is_owner(user))

