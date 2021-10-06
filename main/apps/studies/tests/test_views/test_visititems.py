from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER
from main.apps.users import constants as user_constatnts

from ...models import VisitItem
from ... import constants


class PatientViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(PatientViewsTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.c2 = baker.make('companies.Company')

        self.user_admin = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c1)
        self.user_cra = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c1)
        self.user_admin_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c2)
        self.user_cra_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c2)

        self.study1 = baker.make('studies.Study', company=self.c1, status=constants.STUDY_STATUS_PROGRESS)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        self.visit1 = baker.make('studies.Visit', study=self.study1, arm=self.arm1)
        self.study_item1 = baker.make('studies.StudyItem', study=self.study1)

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

        r = self.client.get(reverse('visititem-list'))
        self.assertEqual(401, r.status_code)

    def test_list_only_for_authenticated_success(self):
        """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """

        self.do_auth_cra_other_company()
        r = self.client.get(reverse('visititem-list'))
        self.assertEqual(200, r.status_code)

    def test_create_cra_failed(self):
        self.do_auth_cra()
        r = self.client.post(reverse('visititem-list'), data={})
        self.assertEqual(403, r.status_code)

    def test_create_admin_success(self):
        data = {
            'visit': self.visit1.id,
            'study_item': self.study_item1.id,
        }

        self.do_auth_admin()
        r = self.client.post(reverse('visititem-list'), data=data)
        self.assertEqual(201, r.status_code)
        qs = VisitItem.objects.all()
        self.assertEqual(1, len(qs))
        obj = qs[0]
        self.assertEqual(self.study1, obj.study)

    def test_patch_cra_fail(self):
        obj = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)

        self.do_auth_cra()
        r = self.client.patch(reverse('visititem-detail', args=(obj.id, )), data={})
        self.assertEqual(403, r.status_code)

    def test_patch_admin_other_fail(self):
        obj = baker.make('studies.VisitItem')  # obj from other company

        self.do_auth_admin()
        r = self.client.patch(reverse('visititem-detail', args=(obj.id, )), data={})
        self.assertEqual(404, r.status_code)  # dostanu 404, protože to odchytí get_queryset

    def test_patch_admin_success(self):
        obj = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)

        data = {
            'visit': self.visit1.id,
            'study_item': self.study_item1.id,
        }

        self.do_auth_admin()
        r = self.client.patch(reverse('visititem-detail', args=(obj.id, )), data=data)
        self.assertEqual(200, r.status_code)
        qs = VisitItem.objects.all()
        obj = qs[0]
        self.assertEqual(obj.visit, self.visit1)
        self.assertEqual(obj.study_item, self.study_item1)

    def test_list_cra_same_company(self):
        obj = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)

        self.do_auth_cra()
        r = self.client.get(reverse('visititem-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj.id, r.data['results'][0]['id'])

    def test_list_cra_other_company(self):
        obj = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)

        self.do_auth_cra_other_company()  # ale přihlašuju se jako jiný uživatel
        r = self.client.get(reverse('visititem-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(0, r.data['pagination']['count'])

    def test_list_admin_same_company(self):
        obj = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)

        self.do_auth_admin()
        r = self.client.get(reverse('visititem-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj.id, r.data['results'][0]['id'])

    def test_list_admin_other_company(self):
        obj = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)

        self.do_auth_admin_other_company()
        r = self.client.get(reverse('visititem-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_delete_admin_success(self):
        obj = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)

        self.do_auth_admin()
        r = self.client.delete(reverse('visititem-detail', args=(obj.id, )))
        self.assertEqual(204, r.status_code)
        self.assertEqual(0, len(VisitItem.objects.active()))
        self.assertEqual(1, len(VisitItem.objects.all()))  # testujeme soft delete

    def test_delete_admin_failed_status(self):
        self.study1.status = constants.STUDY_STATUS_CLOSED
        self.study1.save()
        obj = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)

        self.do_auth_admin()
        r = self.client.delete(reverse('visititem-detail', args=(obj.id, )))

        self.assertEqual(403, r.status_code)

        qs = VisitItem.objects.all()
        self.assertEqual(1, len(qs))
        self.study1.status = constants.STUDY_STATUS_PROGRESS
        self.study1.save()

    def test_delete_cra_failed(self):
        obj = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)

        self.do_auth_cra()
        r = self.client.delete(reverse('visititem-detail', args=(obj.id, )))

        # otestuju, že CRA nemá permission na delete study item
        self.assertEqual(403, r.status_code)
        qs = VisitItem.objects.all()
        self.assertEqual(1, len(qs))
