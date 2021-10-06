from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER
from main.apps.studies.models import Patient
from main.apps.users import constants as user_constatnts

from ... import constants
from ... import utils


class PatientViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(PatientViewsTestCase, self).setUp()
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

        r = self.client.get(reverse('patient-list'))
        self.assertEqual(401, r.status_code)

    def test_list_only_for_authenticated_success(self):
        """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """

        self.do_auth_cra_other_company()
        r = self.client.get(reverse('patient-list'))
        self.assertEqual(200, r.status_code)

    def test_create_cra_failed_bad_data(self):
        s1 = baker.make('studies.Study', company=self.c1, bank_transfer=True)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        self.do_auth_cra()
        data = {
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': 'test',
            'study': str(s1.id),
            'arm': arm.id,
            'site': site.id,
        }
        r = self.client.post(reverse('patient-list'), data=data)
        self.assertEqual(400, r.status_code)

    def test_create_cra_success(self):
        s1 = baker.make('studies.Study', company=self.c1, bank_transfer=True, status=constants.STUDY_STATUS_PROGRESS)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1, cra=self.user_cra)
        self.do_auth_cra()
        data = {
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
            'study': str(s1.id),
            'arm': arm.id,
            'site': site.id,
        }
        r = self.client.post(reverse('patient-list'), data=data)
        self.assertEqual(201, r.status_code)

    def test_create_admin_success(self):
        s1 = baker.make('studies.Study', company=self.c1, bank_transfer=True, status=constants.STUDY_STATUS_PROGRESS)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)

        data = {
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
            'study': str(s1.id),
            'arm': arm.id,
            'site': site.id,
        }

        self.do_auth_admin()
        r = self.client.post(reverse('patient-list'), data=data)
        self.assertEqual(201, r.status_code)
        qs = Patient.objects.all()
        self.assertEqual(1, len(qs))
        obj = qs[0]
        self.assertEqual(s1, obj.study)

    def test_patch_cra_fail(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company, status=constants.STUDY_STATUS_PROGRESS)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1, cra=self.user_cra)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site, number='test123')

        self.do_auth_cra()
        r = self.client.patch(reverse('patient-detail', args=(obj.id, )), data={'number': 'test123'})
        self.assertEqual(200, r.status_code)

    def test_patch_admin_other_fail(self):
        s1 = baker.make('studies.Study', company=self.user_admin_other_company.company)  # nastavím jinou company
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site)

        self.do_auth_admin()
        r = self.client.patch(reverse('patient-detail', args=(obj.id, )), data={})
        self.assertEqual(404, r.status_code)  # dostanu 404, protože to odchytí get_queryset

    def test_patch_admin_success(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_PROGRESS)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site, number='test')
        data = {
            'number': 'test',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
        }

        self.do_auth_admin()
        r = self.client.patch(reverse('patient-detail', args=(obj.id, )), data=data)
        self.assertEqual(200, r.status_code)
        qs = Patient.objects.all()
        obj = qs[0]
        self.assertEqual(obj.number, 'test')
        self.assertEqual(obj.payment_type, PAYMENT_TYPE_BANK_TRANSFER)
        self.assertEqual(obj.payment_info, '7998862/0800')

    def test_list_cra_same_company(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site)

        self.do_auth_cra()
        r = self.client.get(reverse('patient-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj.id, r.data['results'][0]['id'])

    def test_list_cra_other_company(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        _ = baker.make('studies.Patient', study=s1, arm=arm, site=site)

        self.do_auth_cra_other_company()  # ale přihlašuju se jako jiný uživatel
        r = self.client.get(reverse('patient-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_list_admin_same_company(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site)

        self.do_auth_admin()
        r = self.client.get(reverse('patient-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj.id, r.data['results'][0]['id'])

    def test_list_admin_other_company(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        _ = baker.make('studies.Patient', study=s1, arm=arm, site=site)

        self.do_auth_admin_other_company()
        r = self.client.get(reverse('patient-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_delete_admin_success(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_DRAFT)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site)

        self.do_auth_admin()
        r = self.client.delete(reverse('patient-detail', args=(obj.id, )))
        self.assertEqual(405, r.status_code)
        qs = Patient.objects.all()
        self.assertEqual(1, len(qs))

    def test_delete_admin_failed_status(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_PRELAUNCH)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site)

        self.do_auth_admin()
        r = self.client.delete(reverse('patient-detail', args=(obj.id, )))

        self.assertEqual(405, r.status_code)

        qs = Patient.objects.all()
        self.assertEqual(1, len(qs))

    def test_delete_cra_failed(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site)

        self.do_auth_cra()
        r = self.client.delete(reverse('patient-detail', args=(obj.id, )))

        # otestuju, že CRA nemá permission na delete patient
        self.assertEqual(405, r.status_code)
        qs = Patient.objects.all()
        self.assertEqual(1, len(qs))

    def test_patch_doctor_without_sessoin_fail(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_PROGRESS)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site, number='test')
        data = {
            'number': 'test',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': 'testpi',
        }

        r = self.client.patch(reverse('patient-detail', args=(obj.id, )), data=data)
        self.assertEqual(401, r.status_code)

    def test_patch_doctor_with_session_success(self):
        s1 = baker.make('studies.Study', company=self.user_admin.company, status=constants.STUDY_STATUS_PROGRESS)
        
        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj = baker.make('studies.Patient', study=s1, arm=arm, site=site, number='test')
        data = {
            'change_payment_request': True,
        }

        session = self.client.session
        session[settings.DOCTOR_SESSION_KEY] = {
            obj.id: (timezone.now() + timezone.timedelta(minutes=30)).isoformat()
        }
        session.save()

        r = self.client.patch(reverse('patient-detail', args=(obj.id, )), data=data)
        self.assertEqual(200, r.status_code)

    def test_filter_open(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)

        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj1 = baker.make('studies.Patient', study=s1, arm=arm, site=site)
        obj2 = baker.make('studies.Patient', study=s1, arm=arm, site=site)
        baker.make('studies.PatientVisit', visit__visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL, patient=obj1)

        self.do_auth_cra()
        r = self.client.get(reverse('patient-list') + '?active=true')
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj2.id, r.data['results'][0]['id'])

    def test_filter_study(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)

        arm = baker.make('studies.Arm', study=s1)
        site = baker.make('studies.Site', study=s1)
        obj1 = baker.make('studies.Patient', study=s1, arm=arm, site=site)
        obj2 = baker.make('studies.Patient')
        baker.make('studies.PatientVisit', visit__visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL, patient=obj1)

        self.do_auth_cra()
        r = self.client.get(reverse('patient-list') + '?study_id={}'.format(str(s1.id)))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj1.id, r.data['results'][0]['id'])

    def test_filter_change_true(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        obj1 = baker.make('studies.Patient', study=s1)
        obj2 = baker.make('studies.Patient', study=s1)
        utils.mark_patient_as_flagged(obj1)

        self.do_auth_admin()
        r = self.client.get(reverse('patient-list') + '?change_payment=true')
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj1.id, r.data['results'][0]['id'])

    def test_filter_change_false(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        obj1 = baker.make('studies.Patient', study=s1)
        obj2 = baker.make('studies.Patient', study=s1)
        utils.mark_patient_as_flagged(obj1)

        self.do_auth_admin()
        r = self.client.get(reverse('patient-list') + '?change_payment=false')
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj2.id, r.data['results'][0]['id'])

    def test_filter_change_none(self):
        s1 = baker.make('studies.Study', company=self.user_cra.company)
        obj1 = baker.make('studies.Patient', study=s1)
        obj2 = baker.make('studies.Patient', study=s1)
        utils.mark_patient_as_flagged(obj1)

        self.do_auth_admin()
        r = self.client.get(reverse('patient-list'))
        self.assertEqual(2, r.data['pagination']['count'])
