from django.urls import reverse
from django.utils import timezone

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users import constants as user_constatnts

from ..models import CreditBalance
from .. import constants


class CreditBalanceViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        super(CreditBalanceViewSetTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.c2 = baker.make('companies.Company')

        self.user_admin = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c1)
        self.user_cra = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c1)
        self.user_admin_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c2)
        self.user_cra_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c2)

        self.study1 = baker.make('studies.Study', company=self.c1)
        baker.make('studies.Site', cra=self.user_cra, study=self.study1)
        self.study2 = baker.make('studies.Study', company=self.c1)

        self.cb1 = baker.make('credit.CreditBalance', study=self.study1)
        self.cb2 = baker.make('credit.CreditBalance', study=self.study2)
        self.cb3 = baker.make('credit.CreditBalance')

    def do_auth_admin(self):
        self.client.force_authenticate(user=self.user_admin)

    def do_auth_admin_other_company(self):
        self.client.force_authenticate(user=self.user_admin_other_company)

    def do_auth_cra(self):
        self.client.force_authenticate(user=self.user_cra)

    def do_auth_cra_other_company(self):
        self.client.force_authenticate(user=self.user_cra_other_company)

    def test_list_only_for_authenticated_failed(self):
        """ Otestuju, že list endpointy vyžadují přihlášeného uživatele. """

        r = self.client.get(reverse('creditbalance-list'))
        self.assertEqual(401, r.status_code)

    def test_list_only_for_authenticated_success(self):
        """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """

        self.do_auth_cra_other_company()
        r = self.client.get(reverse('creditbalance-list'))
        self.assertEqual(200, r.status_code)

    def test_list_cra_same_company(self):
        self.do_auth_cra()
        r = self.client.get(reverse('creditbalance-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(self.cb1.id, r.data['results'][0]['id'])

    def test_list_cra_other_company(self):
        self.do_auth_cra_other_company()  # ale přihlašuju se jako jiný uživatel
        r = self.client.get(reverse('creditbalance-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_list_admin_same_company(self):
        self.do_auth_admin()
        r = self.client.get(reverse('creditbalance-list'))
        self.assertEqual(2, r.data['pagination']['count'])
        self.assertIn(self.cb1.id, [item['id'] for item in r.data['results']])

    def test_list_admin_other_company(self):
        self.do_auth_admin_other_company()
        r = self.client.get(reverse('creditbalance-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_export_credit_balance(self):
        self.do_auth_admin()
        r = self.client.get(reverse('creditbalance-export'))
        self.assertEqual(200, r.status_code)
        data = r.content.decode()
        self.assertEqual(3, len(data.splitlines()))

    def test_export_credit_balance_with_filter(self):
        self.do_auth_admin()
        date1 = (timezone.now() - timezone.timedelta(days=1)).strftime('%Y-%m-%d')
        date2 = (timezone.now() + timezone.timedelta(days=1)).strftime('%Y-%m-%d')
        r = self.client.get(reverse('creditbalance-export') + "?created_at__date__lte={}&created_at__date__gte={}".format(date2, date1))
        self.assertEqual(200, r.status_code)
        data = r.content.decode()
        self.assertEqual(3, len(data.splitlines()))

    def test_export_credit_balance_with_filter_empty(self):
        self.do_auth_admin()
        date1 = (timezone.now() + timezone.timedelta(days=1)).strftime('%Y-%m-%d')
        date2 = (timezone.now() - timezone.timedelta(days=1)).strftime('%Y-%m-%d')
        r = self.client.get(reverse('creditbalance-export') + "?created_at__date__lte={}&created_at__date__gte={}".format(date2, date1))
        self.assertEqual(200, r.status_code)
        data = r.content.decode()
        self.assertEqual(1, len(data.splitlines()))

    def test_export_credit_balance_with_exact_dates(self):
        self.do_auth_admin()
        date1 = timezone.now().strftime('%Y-%m-%d')
        date2 = timezone.now().strftime('%Y-%m-%d')
        r = self.client.get(reverse('creditbalance-export') + "?created_at__date__lte={}&created_at__date__gte={}".format(date2, date1))
        self.assertEqual(200, r.status_code)
        data = r.content.decode()
        self.assertEqual(3, len(data.splitlines()))

    def test_export_credit_balance_with_study_id_filter(self):
        self.do_auth_admin()
        r = self.client.get(reverse('creditbalance-export') + "?study_id={}".format(str(self.study2.id)))
        self.assertEqual(200, r.status_code)
        data = r.content.decode()
        self.assertEqual(2, len(data.splitlines()))
