from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER
from main.apps.users import constants as user_constatnts
from main.apps.studies import constants as study_constants

from ...models import VisitItem, PatientVisit, PatientVisitItem
from ... import constants


class PatientViewsItemTestCase(APITestCase):

    def setUp(self) -> None:
        super(PatientViewsItemTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.c2 = baker.make('companies.Company')

        self.user_admin = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c1)
        self.user_cra = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c1)
        self.user_admin_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_ADMIN, company=self.c2)
        self.user_cra_other_company = baker.make('users.User', role=user_constatnts.USER_ROLE_CRA, company=self.c2)

        self.study1 = baker.make('studies.Study', company=self.c1, status=study_constants.STUDY_STATUS_PROGRESS)
        self.site1 = baker.make('studies.Site', study=self.study1, cra=self.user_cra)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        self.patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=self.site1)
        self.visit1 = baker.make('studies.Visit', study=self.study1, arm=self.arm1)
        self.study_item1 = baker.make('studies.StudyItem', study=self.study1, price=100)
        self.visit_item = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1,
                                     study_item=self.study_item1)
        self.patient_visit = baker.make('studies.PatientVisit', patient=self.patient1, visit=self.visit1,
                                        study=self.study1)

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

        r = self.client.get(reverse('patientvisititem-list'))
        self.assertEqual(401, r.status_code)

    def test_list_only_for_authenticated_success(self):
        """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """

        self.do_auth_cra_other_company()
        r = self.client.get(reverse('patientvisititem-list'))
        self.assertEqual(200, r.status_code)

    def test_create_cra_success(self):
        data = {
            'visit_item': self.visit_item.id,
            'patient_visit': self.patient_visit.id,
        }

        self.do_auth_cra()
        r = self.client.post(reverse('patientvisititem-list'), data=data)
        self.assertEqual(201, r.status_code)
        qs = PatientVisitItem.objects.all()
        self.assertEqual(1, len(qs))
        obj = qs[0]
        self.assertEqual(self.patient_visit, obj.patient_visit)

    def test_list_cra_same_company(self):
        obj = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item)

        self.do_auth_cra()
        r = self.client.get(reverse('patientvisititem-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj.id, r.data['results'][0]['id'])

    def test_list_cra_other_company(self):
        # vytvořím item bez definice patient visit, takže nepatří určitě přihlášenému CRA
        _ = baker.make('studies.PatientVisitItem', visit_item=self.visit_item)

        self.do_auth_cra_other_company()  # ale přihlašuju se jako jiný uživatel
        r = self.client.get(reverse('patientvisit-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_list_admin_same_company(self):
        obj = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item)

        self.do_auth_admin()
        r = self.client.get(reverse('patientvisititem-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj.id, r.data['results'][0]['id'])

    def test_list_admin_other_company(self):
        # vytvořím item bez definice patient visit, takže nepatří určitě přihlášenému ADMIN
        _ = baker.make('studies.PatientVisitItem', visit_item=self.visit_item)

        self.do_auth_admin_other_company()
        r = self.client.get(reverse('patientvisititem-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_patch_approved_failed(self):
        obj = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item)
        data = {
            'approved': True,
        }
        self.do_auth_cra()
        r = self.client.patch(reverse('patientvisititem-detail', args=(obj.id, )), data=data)
        self.assertEqual(400, r.status_code)
        obj.refresh_from_db()
        self.assertFalse(obj.approved)

    def test_patch_approved_success(self):
        baker.make('credit.CreditBalance', balance_sum=1000 * settings.INT_RATIO, study=self.study1)
        obj = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item)
        data = {
            'approved': True,
        }
        self.do_auth_cra()
        r = self.client.patch(reverse('patientvisititem-detail', args=(obj.id, )), data=data)
        self.assertEqual(200, r.status_code)
        obj.refresh_from_db()
        self.assertTrue(obj.approved)

    def test_patch_admin_other_company(self):
        obj = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item)
        data = {
            'approved': True,
        }
        self.do_auth_admin_other_company()
        r = self.client.patch(reverse('patientvisititem-detail', args=(obj.id, )), data=data)
        self.assertEqual(404, r.status_code)

    def test_patch_cra_same_company_other_owner(self):
        site = baker.make('studies.Site', study=self.study1)
        patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site)
        patient_visit = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        obj = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item)
        data = {
            'approved': True,
        }
        self.do_auth_cra()
        r = self.client.patch(reverse('patientvisititem-detail', args=(obj.id, )), data=data)
        self.assertEqual(404, r.status_code)

    def test_filter_approved_none(self):
        site = baker.make('studies.Site', study=self.study1, cra=self.user_cra)
        patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site)
        patient_visit = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=True)
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=False)
        obj3 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=None)
        self.do_auth_cra()
        r = self.client.get(reverse('patientvisititem-list') + '?approved=none')
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj3.id, r.data['results'][0]['id'])

    def test_filter_approved_any(self):
        site = baker.make('studies.Site', study=self.study1, cra=self.user_cra)
        patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site)
        patient_visit = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=True)
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=False)
        obj3 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=None)
        self.do_auth_cra()
        r = self.client.get(reverse('patientvisititem-list') + '?approved=any')
        self.assertEqual(200, r.status_code)
        self.assertEqual(2, r.data['pagination']['count'])
        result_id_list = [item['id'] for item in r.data['results']]
        self.assertIn(obj1.id, result_id_list)
        self.assertIn(obj2.id, result_id_list)

    def test_filter_approved_false(self):
        site = baker.make('studies.Site', study=self.study1, cra=self.user_cra)
        patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site)
        patient_visit = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=True)
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=False)
        obj3 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=None)
        self.do_auth_cra()
        r = self.client.get(reverse('patientvisititem-list') + '?approved=false')
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj2.id, r.data['results'][0]['id'])

    def test_filter_approved_true(self):
        site = baker.make('studies.Site', study=self.study1, cra=self.user_cra)
        patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site)
        patient_visit = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=True)
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=False)
        obj3 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, approved=None)
        self.do_auth_cra()
        r = self.client.get(reverse('patientvisititem-list') + '?approved=true')
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj1.id, r.data['results'][0]['id'])

    def test_filter_patient_visit__patient__site__title(self):
        site = baker.make('studies.Site', study=self.study1, cra=self.user_cra, title='test_site')
        site2 = baker.make('studies.Site', study=self.study1, cra=self.user_cra, title='test_site_2')
        patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site)
        patient2 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site2)
        patient_visit = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        patient_visit2 = baker.make('studies.PatientVisit', patient=patient2, visit=self.visit1, study=self.study1)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item)
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit2, visit_item=self.visit_item)
        self.do_auth_cra()
        r = self.client.get(reverse('patientvisititem-list') + '?patient_visit__patient__site__id={}'.format(site.id))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj1.id, r.data['results'][0]['id'])

    def test_filter_patient_visit__patient__id(self):
        site = baker.make('studies.Site', study=self.study1, cra=self.user_cra, title='test_site')
        patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site, number='test_patient')
        patient2 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site, number='test_patient_2')
        patient_visit = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        patient_visit2 = baker.make('studies.PatientVisit', patient=patient2, visit=self.visit1, study=self.study1)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item)
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit2, visit_item=self.visit_item)
        self.do_auth_cra()
        r = self.client.get(reverse('patientvisititem-list') + '?patient_visit__patient__id={}'.format(patient1.id))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj1.id, r.data['results'][0]['id'])

    def test_filter_payment_status(self):
        site = baker.make('studies.Site', study=self.study1, cra=self.user_cra, title='test_site')
        patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site, number='test_patient')
        patient_visit = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, payment_status='WAITING')
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, payment_status='SENT')
        self.do_auth_cra()
        r = self.client.get(reverse('patientvisititem-list') + '?payment_status=SENT')
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj2.id, r.data['results'][0]['id'])

    def test_filter_patient_visit(self):
        site = baker.make('studies.Site', study=self.study1, cra=self.user_cra, title='test_site')
        patient1 = baker.make('studies.Patient', study=self.study1, arm=self.arm1, site=site, number='test_patient')
        patient_visit = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        patient_visit2 = baker.make('studies.PatientVisit', patient=patient1, visit=self.visit1, study=self.study1)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit, visit_item=self.visit_item, payment_status='WAITING')
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=patient_visit2, visit_item=self.visit_item, payment_status='SENT')
        self.do_auth_cra()
        r = self.client.get(reverse('patientvisititem-list') + '?patient_visit={}'.format(patient_visit.id))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(obj1.id, r.data['results'][0]['id'])
