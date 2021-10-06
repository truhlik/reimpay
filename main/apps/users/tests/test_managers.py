from django.test import TestCase

from model_bakery import baker

from .. import constants
from .. import models


class UserManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(UserManagerTestCase, self).setUp()
        self.user_admin = baker.make('users.User', role=constants.USER_ROLE_ADMIN)
        self.user_cra = baker.make('users.User', role=constants.USER_ROLE_CRA)

    def do_auth_admin(self):
        self.client.force_authenticate(user=self.user_admin)

    def do_auth_cra(self):
        self.client.force_authenticate(user=self.user_cra)

    def test_owner_by_admin(self):
        company1 = baker.make('companies.Company')
        company1.users.set([self.user_admin, self.user_cra])
        qs = models.User.objects.owner(self.user_admin)
        self.assertEqual(2, len(qs))

    def test_owner_by_cra(self):
        company1 = baker.make('companies.Company')
        company1.users.set([self.user_admin, self.user_cra])
        qs = models.User.objects.owner(self.user_cra)
        self.assertEqual(1, len(qs))
