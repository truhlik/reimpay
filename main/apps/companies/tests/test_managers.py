from django.test import TestCase

from model_bakery import baker

from main.apps.users import constants as user_constants

from ..models import Company
from .. import constants


class CompanyManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(CompanyManagerTestCase, self).setUp()

    def test_owner_single(self):
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN)
        company1 = baker.make('companies.Company')
        company1.users.set([user])
        company2 = baker.make('companies.Company')
        qs = Company.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(company1.id, qs[0].id)

