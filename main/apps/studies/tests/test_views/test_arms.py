from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users import constants as user_constatnts

from ...models import Arm
from ... import constants


class ArmsViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(ArmsViewsTestCase, self).setUp()
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

        r = self.client.get(reverse('arm-list'))
        self.assertEqual(401, r.status_code)

    def test_list_only_for_authenticated_success(self):
        """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """

        self.do_auth_cra_other_company()
        r = self.client.get(reverse('arm-list'))
        self.assertEqual(200, r.status_code)

    def test_create_cra_failed(self):
        self.do_auth_cra()
        r = self.client.post(reverse('arm-list'), data={})
        self.assertEqual(403, r.status_code)

    def test_create_admin_success(self):
        self.study1 = baker.make('studies.Study', company=self.c1)

        data = {
            'title': 'test',
            'max_unscheduled': 100,
            'study': str(self.study1.id),
        }

        self.do_auth_admin()
        r = self.client.post(reverse('arm-list'), data=data)
        self.assertEqual(201, r.status_code)
        qs = Arm.objects.all()
        self.assertEqual(1, len(qs))
        obj = qs[0]
        self.assertEqual(self.study1, obj.study)
        self.assertEqual(3, obj.visits.all().count())

    def test_patch_cra_fail(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_cra()
        r = self.client.patch(reverse('arm-detail', args=(arm.id, )), data={})
        self.assertEqual(403, r.status_code)

    def test_patch_admin_other_fail(self):
        s1 = baker.make('studies.Study', company=self.user_admin_other_company.company)  # nastavím jinou company
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_admin()
        r = self.client.patch(reverse('arm-detail', args=(arm.id, )), data={})
        self.assertEqual(404, r.status_code)  # dostanu 404, protože to odchytí get_queryset

    def test_patch_admin_success(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company)
        arm = baker.make('studies.Arm', study=s1)
        data = {
            'title': 'test',
            'max_unscheduled': 100,
        }

        self.do_auth_admin()
        r = self.client.patch(reverse('arm-detail', args=(arm.id, )), data=data)
        self.assertEqual(200, r.status_code)
        qs = Arm.objects.all()
        obj = qs[0]
        self.assertEqual(obj.title, 'test')
        self.assertEqual(obj.max_unscheduled, 100)

    def test_list_cra_same_company(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_cra()
        r = self.client.get(reverse('arm-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(arm.id, r.data['results'][0]['id'])

    def test_list_cra_other_company(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_cra_other_company()  # ale přihlašuju se jako jiný uživatel
        r = self.client.get(reverse('arm-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(0, r.data['pagination']['count'])

    def test_list_admin_same_company(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company)
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_admin()
        r = self.client.get(reverse('arm-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(arm.id, r.data['results'][0]['id'])

    def test_list_admin_other_company(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company)
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_admin_other_company()
        r = self.client.get(reverse('arm-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_delete_admin_success(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_DRAFT)
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_admin()
        r = self.client.delete(reverse('arm-detail', args=(arm.id, )))
        self.assertEqual(204, r.status_code)
        qs = Arm.objects.all()
        self.assertEqual(0, len(qs))

    def test_delete_admin_success_status(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_PROGRESS)
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_admin()
        r = self.client.delete(reverse('arm-detail', args=(arm.id, )))

        self.assertEqual(204, r.status_code)

        arm.refresh_from_db()
        self.assertTrue(arm.deleted)

    def test_delete_admin_failed_status(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_BILLING)
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_admin()
        r = self.client.delete(reverse('arm-detail', args=(arm.id, )))

        self.assertEqual(403, r.status_code)

        qs = Arm.objects.all()
        self.assertEqual(1, len(qs))

    def test_delete_cra_failed(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        arm = baker.make('studies.Arm', study=s1)

        self.do_auth_cra()
        r = self.client.delete(reverse('arm-detail', args=(arm.id, )))

        # otestuju, že CRA nemá permission na delete study item
        self.assertEqual(403, r.status_code)
        qs = Arm.objects.all()
        self.assertEqual(1, len(qs))
