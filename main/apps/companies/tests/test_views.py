import json
from collections import OrderedDict

from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users import constants as user_constatnts


class CompanyViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(CompanyViewsTestCase, self).setUp()
        c = baker.make('companies.Company')
        self.user_admin = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=c)
        self.user_cra = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA)

    def do_auth_admin(self):
        self.client.force_authenticate(user=self.user_admin)

    def do_auth_cra(self):
        self.client.force_authenticate(user=self.user_cra)

    def test_company_list_only_for_authenticated_failed(self):
        """ Otestuju, že Company endpointy vyžadují přihlášeného uživatele. """

        r = self.client.get(reverse('company-list'))
        self.assertEqual(401, r.status_code)

    def test_company_list_only_for_authenticated_success(self):
        """ Otestuju, že Company endpointy vyžadují přihlášeného uživatele. """

        self.do_auth_admin()
        r = self.client.get(reverse('company-list'))
        self.assertEqual(200, r.status_code)

    def test_company_patch(self):
        c1 = baker.make('companies.Company', description='')
        c1.users.set([self.user_admin])
        data = {'description': 'test'}
        self.do_auth_admin()
        r = self.client.patch(reverse('company-detail', args=(c1.id, )), data=data)
        self.assertEqual(405, r.status_code)

    def test_company_patch_primary(self):
        c1 = baker.make('companies.Company', description='')
        c1.users.set([self.user_admin])
        data = {'description': 'test'}
        self.do_auth_admin()
        r = self.client.patch(reverse('company-primary'), data=data)
        self.assertEqual(405, r.status_code)

    def test_company_patch_primary_as_cra_fail(self):
        c1 = baker.make('companies.Company', description='')
        c1.users.set([self.user_cra])
        data = {'description': 'test'}
        self.do_auth_cra()
        r = self.client.patch(reverse('company-primary'), data=data)
        self.assertEqual(403, r.status_code)

    def test_companies_list_owner(self):
        company1 = baker.make('companies.Company')
        company1.users.set([self.user_admin])
        company2 = baker.make('companies.Company')

        self.do_auth_admin()
        r = self.client.get(reverse('company-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(company1.id, r.data['results'][0]['id'])

    def test_companies_list_cra(self):
        company1 = baker.make('companies.Company')
        company1.users.set([self.user_cra])
        company2 = baker.make('companies.Company')

        self.do_auth_cra()
        r = self.client.get(reverse('company-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(company1.id, r.data['results'][0]['id'])
