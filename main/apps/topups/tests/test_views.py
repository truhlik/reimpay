from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.topups.models import TopUp
from main.apps.users import constants as user_constatnts


class TopUpViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(TopUpViewsTestCase, self).setUp()
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

    def test_get_for_authorized_admin_success(self):
        self.do_auth_admin()
        r = self.client.get(reverse('topup-list'))
        self.assertEqual(200, r.status_code)

    def test_get_for_unauthorized_admin_failed(self):
        r = self.client.get(reverse('topup-list'))
        self.assertEqual(401, r.status_code)

    def test_get_for_authorized_cra_failed(self):
        self.do_auth_cra()
        r = self.client.get(reverse('topup-list'))
        self.assertEqual(200, r.status_code)

    def test_get_for_authorized_cra_failed_data(self):
        study1 = baker.make('studies.Study', company=self.user_cra.company)
        t1 = baker.make(TopUp, study=study1)

        self.do_auth_cra()
        r = self.client.get(reverse('topup-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, len(r.data['results']))

    def test_get_for_authorized_admin_data(self):

        c = baker.make('companies.Company')
        study1 = baker.make('studies.Study', company=self.user_admin.company)
        t1 = baker.make(TopUp, study=study1)

        self.do_auth_admin()
        r = self.client.get(reverse('topup-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, len(r.data['results']))

    def test_create_as_admin(self):
        data = {
            'study': str(self.study1.id),
            'amount': 10000,
        }

        self.do_auth_admin()
        r = self.client.post(reverse('topup-list'), data=data)
        self.assertEqual(201, r.status_code)
        qs = TopUp.objects.all()
        self.assertEqual(1, len(qs))

    def test_create_as_cra(self):
        data = {
            'study': str(self.study1.id),
            'amount': 10000,
        }

        self.do_auth_cra()
        r = self.client.post(reverse('topup-list'), data=data)
        self.assertEqual(201, r.status_code)
        qs = TopUp.objects.all()
        self.assertEqual(1, len(qs))

    def test_site_patient_contract_pdf_get_without_auth(self):
        topup = baker.make('topups.TopUp')
        r = self.client.get(reverse('topup-pdf', args=(topup.pk, )))
        self.assertEqual(401, r.status_code)

    def test_site_patient_contract_pdf_get_with_auth_from_other_company(self):
        topup = baker.make('topups.TopUp')
        self.do_auth_admin_other_company()
        r = self.client.get(reverse('topup-pdf', args=(topup.pk, )))
        self.assertEqual(404, r.status_code)

    # todo
    # def test_site_patient_contract_pdf_get_with_auth(self):
    #     s1 = baker.make('studies.Study', company=self.user_admin.company)
    #     self.do_auth_admin()
    #     topup = baker.make('topups.TopUp', study=s1)
    #     r = self.client.get(reverse('topup-pdf', args=(topup.pk, )))
    #     self.assertEqual(200, r.status_code)
    #     self.assertEqual(', "application/pdf"', r._content_type_for_repr)
