from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users import constants as user_constatnts


class InvoiceViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        super(InvoiceViewSetTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.c2 = baker.make('companies.Company')

        self.user_admin = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c1)
        self.user_cra = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c1)
        self.user_admin_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c2)
        self.user_cra_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c2)

        self.invoice1 = baker.make('invoices.Invoice', company=self.c1)
        self.invoice2 = baker.make('invoices.Invoice', company=self.c2)

    def do_auth_admin(self):
        self.client.force_authenticate(user=self.user_admin)

    def do_auth_admin_other_company(self):
        self.client.force_authenticate(user=self.user_admin_other_company)

    def do_auth_cra(self):
        self.client.force_authenticate(user=self.user_cra)

    def do_auth_cra_other_company(self):
        self.client.force_authenticate(user=self.user_cra_other_company)

    def test_list_only_for_authenticated_failed(self):
        """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """

        r = self.client.get(reverse('creditbalance-list'))
        self.assertEqual(401, r.status_code)

    def test_list_only_for_authenticated_success(self):
        """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """

        self.do_auth_admin_other_company()
        r = self.client.get(reverse('invoice-list'))
        self.assertEqual(200, r.status_code)

    def test_list_cra_same_company(self):
        self.do_auth_cra()
        r = self.client.get(reverse('invoice-list'))
        self.assertEqual(403, r.status_code)

    def test_list_cra_other_company(self):
        self.do_auth_cra_other_company()  # ale přihlašuju se jako jiný uživatel
        r = self.client.get(reverse('invoice-list'))
        self.assertEqual(403, r.status_code)

    def test_list_admin_same_company(self):
        self.do_auth_admin()
        r = self.client.get(reverse('invoice-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertIn(self.invoice1.id, [item['id'] for item in r.data['results']])

    def test_list_admin_other_company(self):
        self.do_auth_admin_other_company()
        r = self.client.get(reverse('invoice-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertIn(self.invoice2.id, [item['id'] for item in r.data['results']])

    def test_retrieve(self):
        self.do_auth_admin()
        r = self.client.get(reverse('invoice-detail', args=(self.invoice1.id, )))
        self.assertEqual(200, r.status_code)
        self.assertEqual(self.invoice1.id, r.data['id'])
