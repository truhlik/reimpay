import datetime

from django.test import Client
from django.urls import reverse
from django.utils import timezone

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users import constants as user_constatnts


class CoreViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(CoreViewsTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.c2 = baker.make('companies.Company')

        self.user_admin = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c1)
        self.user_cra = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c1)
        self.user_admin_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c2)
        self.user_cra_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c2)

        self.study1 = baker.make('studies.Study', company=self.c1)
        self.study2 = baker.make('studies.Study', company=self.c1)

        self.cb1 = baker.make('credit.CreditBalance', study=self.study1)
        self.cb2 = baker.make('credit.CreditBalance', study=self.study2)
        self.cb3 = baker.make('credit.CreditBalance')

        self.site = baker.make('studies.Site', study=self.study1, cra=self.user_cra)

    def do_auth_admin(self):
        self.client.force_authenticate(user=self.user_admin)

    def do_auth_admin_other_company(self):
        self.client.force_authenticate(user=self.user_admin_other_company)

    def do_auth_cra(self):
        self.client.force_authenticate(user=self.user_cra)

    def do_auth_cra_other_company(self):
        self.client.force_authenticate(user=self.user_cra_other_company)

    # def test_list_only_for_authenticated_failed(self):
    #     """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """
    #
    #     r = self.client.get(reverse('topup-list'))
    #     self.assertEqual(401, r.status_code)
    #
    # def test_list_only_for_authenticated_success(self):
    #     """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """
    #
    #     self.do_auth_cra_other_company()
    #     r = self.client.get(reverse('topup-list'))
    #     self.assertEqual(200, r.status_code)

    def test_retrieve_finance(self):
        self.do_auth_admin()
        r = self.client.get(reverse('finance-detail', args=(self.study1.id, )))
        self.assertEqual(200, r.status_code)
        for k in ['actual_balance', 'paid', 'remaining_visits', 'avg_visit_value', 'exp_budget_need']:
            self.assertIn(k, r.data.keys())

    def test_retrieve_finance_by_cra(self):
        self.do_auth_cra()
        r = self.client.get(reverse('finance-detail', args=(self.study1.id, )))
        self.assertEqual(200, r.status_code)
        for k in ['actual_balance', 'paid', 'remaining_visits', 'avg_visit_value', 'exp_budget_need']:
            self.assertIn(k, r.data.keys())

    def test_doctor_login_view(self):
        patient = baker.make('studies.Patient', number='1', site__pin='2')
        data = {
            'patient_number': 1,
            'site_pin': 2,
        }
        client = Client()
        r = client.post(reverse('doctor-login'), data=data)
        self.assertEqual(200, r.status_code)
        self.assertEqual('/app/#/patient/{}/'.format(patient.id), r.json()['redirect_to'])
        session = client.session
        dt = datetime.datetime.fromisoformat(session["patients"][str(patient.id)])
        self.assertTrue(dt > timezone.now())

    def test_retrieve_stats(self):
        self.do_auth_admin()
        r = self.client.get(reverse('finance-stats', args=(self.study1.id, )))
        self.assertEqual(200, r.status_code)
        for k in ['stats']:
            self.assertIn(k, r.data.keys())

    def test_retrieve_stats_by_cra(self):
        self.do_auth_cra()
        r = self.client.get(reverse('finance-stats', args=(self.study1.id, )))
        self.assertEqual(200, r.status_code)
        for k in ['stats']:
            self.assertIn(k, r.data.keys())
