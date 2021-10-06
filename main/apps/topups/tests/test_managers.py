from django.test import TestCase

from model_bakery import baker

from main.apps.users import constants as user_constants

from ..models import TopUp


class TopUpManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(TopUpManagerTestCase, self).setUp()

    def test_owner(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        t1 = baker.make(TopUp, study=study1)
        _ = baker.make(TopUp)

        qs = TopUp.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(t1, qs[0])

    def test_owner_as_cra(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        baker.make('studies.Site', cra=user, study=study1)

        t1 = baker.make(TopUp, study=study1)
        _ = baker.make(TopUp)

        qs = TopUp.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(t1, qs[0])
