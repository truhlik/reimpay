from django.test import TestCase

from model_bakery import baker

from main.apps.users import constants as user_constants

from ... import constants


class StudyModelTestCase(TestCase):

    def setUp(self) -> None:
        super(StudyModelTestCase, self).setUp()

    def test_is_owner_admin_associated_with_this_study(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        self.assertTrue(study1.is_owner(user))

    def test_is_owner_cra_associated_with_this_study(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        baker.make('studies.Site', cra=user, study=study1)
        self.assertTrue(study1.is_owner(user))

    def test_is_owner_cra_not_associated(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        self.assertFalse(study1.is_owner(user))

    def test_is_owner_admin_not_associated_with_this_study(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c2)
        study1 = baker.make('studies.Study', company=c)
        self.assertFalse(study1.is_owner(user))

