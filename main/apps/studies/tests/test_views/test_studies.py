from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users import constants as user_constatnts

from ...models import Study
from ... import constants


class StudyViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(StudyViewsTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.c2 = baker.make('companies.Company')

        self.user_admin = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c1)
        self.user_cra = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c1)
        self.user_admin_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c2)
        self.user_cra_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c2)

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

        r = self.client.get(reverse('study-list'))
        self.assertEqual(401, r.status_code)

    def test_list_only_for_authenticated_success(self):
        """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """

        self.do_auth_cra_other_company()
        r = self.client.get(reverse('study-list'))
        self.assertEqual(200, r.status_code)

    def test_create_cra_failed(self):
        self.do_auth_cra()
        r = self.client.post(reverse('study-list'), data={})
        self.assertEqual(403, r.status_code)

    def test_create_admin_success(self):
        data = {
            'number': '1',
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': False,
            'pay_frequency': 2,
            'bank_account': '7998862/0800',
        }

        self.do_auth_admin()
        r = self.client.post(reverse('study-list'), data=data)
        self.assertEqual(201, r.status_code)
        qs = Study.objects.all()
        self.assertEqual(1, len(qs))
        obj = qs[0]
        self.assertEqual(self.user_admin.company, obj.company)
        exp_data = {
            'status': constants.STUDY_STATUS_DRAFT,
            'number': '1',
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': False,
            'pay_frequency': 2,
        }
        db_data = {
            'status': obj.status,
            'number': obj.number,
            'identifier': obj.identifier,
            'notes': obj.notes,
            'bank_transfer': obj.bank_transfer,
            'post_office_cash': obj.post_office_cash,
            'pay_frequency': obj.pay_frequency,
        }
        self.assertDictEqual(exp_data, db_data)

    def test_patch_cra_fail(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        s1 = baker.make('studies.Site', cra=self.user_cra, study=s1)
        self.do_auth_cra()
        r = self.client.patch(reverse('study-detail', args=(s1.id, )), data={})
        self.assertEqual(403, r.status_code)

    def test_patch_admin_other_fail(self):
        s1 = baker.make('studies.Study', company=self.user_admin_other_company.company)  # nastavím jinou company
        self.do_auth_admin()
        r = self.client.patch(reverse('study-detail', args=(s1.id, )), data={})
        self.assertEqual(404, r.status_code)  # dostanu 404, protože to odchytí get_queryset

    def test_patch_admin_success(self):
        data = {
            'number': '1',
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': False,
            'pay_frequency': 2,
        }
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_PROGRESS)
        self.do_auth_admin()
        r = self.client.patch(reverse('study-detail', args=(s1.id, )), data=data)
        self.assertEqual(200, r.status_code)
        qs = Study.objects.all()
        obj = qs[0]
        self.assertEqual(self.user_admin.company, obj.company)
        exp_data = {
            'status': constants.STUDY_STATUS_PROGRESS,
            'number': '1',
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': False,
            'pay_frequency': 2,
        }
        db_data = {
            'status': obj.status,
            'number': obj.number,
            'identifier': obj.identifier,
            'notes': obj.notes,
            'bank_transfer': obj.bank_transfer,
            'post_office_cash': obj.post_office_cash,
            'pay_frequency': obj.pay_frequency,
        }
        self.assertDictEqual(exp_data, db_data)

    def test_patch_admin_fail_because_of_status(self):
        data = {
            'number': '1',
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': False,
            'pay_frequency': 2,
        }
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_BILLING)
        self.do_auth_admin()
        r = self.client.patch(reverse('study-detail', args=(s1.id, )), data=data)
        self.assertEqual(403, r.status_code)

    def test_list_cra_same_company(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        _ = baker.make('studies.Site', cra=self.user_cra, study=s1)
        _ = baker.make('studies.Study', company=self.user_cra.company)
        self.do_auth_cra()
        r = self.client.get(reverse('study-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(str(s1.id), r.data['results'][0]['id'])

    def test_list_cra_other_company(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        self.do_auth_cra_other_company()  # ale přihlašuju se jako jiný uživatel
        r = self.client.get(reverse('study-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_list_admin_same_company(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company)
        self.do_auth_admin()
        r = self.client.get(reverse('study-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(str(s1.id), r.data['results'][0]['id'])

    def test_list_admin_other_company(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company)
        self.do_auth_admin_other_company()
        r = self.client.get(reverse('study-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_delete_admin_success(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_DRAFT)
        self.do_auth_admin()
        r = self.client.delete(reverse('study-detail', args=(s1.id, )))
        self.assertEqual(204, r.status_code)
        qs = Study.objects.all()
        self.assertEqual(0, len(qs))

    def test_delete_admin_failed_status(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_PROGRESS)
        self.do_auth_admin()
        r = self.client.delete(reverse('study-detail', args=(s1.id, )))
        self.assertEqual(204, r.status_code)
        qs = Study.objects.all()
        self.assertEqual(1, len(qs))

    def test_delete_cra_failed(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        s1 = baker.make('studies.Site', cra=self.user_cra, study=s1)
        self.do_auth_cra()
        r = self.client.delete(reverse('study-detail', args=(s1.id, )))
        self.assertEqual(403, r.status_code)
        qs = Study.objects.all()
        self.assertEqual(1, len(qs))

    def test_config_cra(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        _ = baker.make('studies.Site', cra=self.user_cra, study=s1)
        self.do_auth_cra()
        r = self.client.get(reverse('study-config', args=(s1.id, )))
        self.assertEqual(200, r.status_code)

    def test_config_admin(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company)
        self.do_auth_admin()
        r = self.client.get(reverse('study-config', args=(s1.id, )))
        self.assertEqual(200, r.status_code)
        self.assertTrue('config' in r.data.keys())
