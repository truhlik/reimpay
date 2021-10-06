from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users import constants as user_constatnts
from main.apps.studies import constants as study_constants

from ...models import VisitItem, PatientVisit
from ... import constants


class PatientVisitViewsTestCase(APITestCase):

    def setUp(self) -> None:
        super(PatientVisitViewsTestCase, self).setUp()
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

        r = self.client.get(reverse('patientvisit-list'))
        self.assertEqual(401, r.status_code)

    def test_list_only_for_authenticated_success(self):
        """ Otestuju, že Study endpointy vyžadují přihlášeného uživatele. """

        self.do_auth_cra_other_company()
        r = self.client.get(reverse('patientvisit-list'))
        self.assertEqual(200, r.status_code)

    def test_create_cra_success(self):
        visit = baker.make('studies.Visit', arm=self.arm1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit_item = baker.make('studies.VisitItem', visit=visit)
        visit_item2 = baker.make('studies.VisitItem', visit=visit)
        visit_item3 = baker.make('studies.VisitItem', visit=visit)

        data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
            'visit_items': [visit_item.id, visit_item2.id, visit_item3.id]
        }

        self.do_auth_cra()
        r = self.client.post(reverse('patientvisit-list'), data=data)
        self.assertEqual(201, r.status_code)
        qs = PatientVisit.objects.all()
        self.assertEqual(1, len(qs))
        obj = qs[0]
        self.assertEqual(self.study1, obj.study)

    def test_list_cra_same_company(self):
        obj = baker.make('studies.PatientVisit', study=self.study1, visit=self.visit1, patient=self.patient1)
        _ = baker.make('studies.PatientVisit')

        self.do_auth_cra()
        r = self.client.get(reverse('patientvisit-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(str(obj.id), r.data['results'][0]['id'])

    def test_list_cra_other_company(self):
        obj = baker.make('studies.PatientVisit', study=self.study1, visit=self.visit1, patient=self.patient1)

        self.do_auth_cra_other_company()  # ale přihlašuju se jako jiný uživatel
        r = self.client.get(reverse('patientvisit-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_list_admin_same_company(self):
        obj = baker.make('studies.PatientVisit', study=self.study1, visit=self.visit1, patient=self.patient1)
        _ = baker.make('studies.PatientVisit')

        self.do_auth_admin()
        r = self.client.get(reverse('patientvisit-list'))
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(str(obj.id), r.data['results'][0]['id'])

    def test_list_admin_other_company(self):
        obj = baker.make('studies.PatientVisit', study=self.study1, visit=self.visit1, patient=self.patient1)
        _ = baker.make('studies.PatientVisit')

        self.do_auth_admin_other_company()
        r = self.client.get(reverse('patientvisit-list'))
        self.assertEqual(0, r.data['pagination']['count'])

    def test_list_doctor_with_session(self):
        obj = baker.make('studies.PatientVisit', study=self.study1, visit=self.visit1, patient=self.patient1)
        _ = baker.make('studies.PatientVisit')

        session = self.client.session
        session[settings.DOCTOR_SESSION_KEY] = {
            self.patient1.id: (timezone.now() + timezone.timedelta(minutes=30)).isoformat()
        }
        session.save()

        r = self.client.get(reverse('patientvisit-list') + '?patient_id={}'.format(self.patient1.id))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])

    def test_create_doctor_without_session_fail(self):
        visit = baker.make('studies.Visit', arm=self.arm1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit_item = baker.make('studies.VisitItem', visit=visit)
        visit_item2 = baker.make('studies.VisitItem', visit=visit)
        visit_item3 = baker.make('studies.VisitItem', visit=visit)

        data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
            'visit_items': [visit_item.id, visit_item2.id, visit_item3.id]
        }

        r = self.client.post(reverse('patientvisit-list'), data=data)
        self.assertEqual(401, r.status_code)

    def test_create_doctor_with_session_success(self):
        visit = baker.make('studies.Visit', arm=self.arm1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit_item = baker.make('studies.VisitItem', visit=visit)
        visit_item2 = baker.make('studies.VisitItem', visit=visit)
        visit_item3 = baker.make('studies.VisitItem', visit=visit)

        session = self.client.session
        session[settings.DOCTOR_SESSION_KEY] = {
            self.patient1.id: (timezone.now() + timezone.timedelta(minutes=30)).isoformat()
        }
        session.save()

        data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
            'visit_items': [visit_item.id, visit_item2.id, visit_item3.id]
        }

        r = self.client.post(reverse('patientvisit-list'), data=data)
        self.assertEqual(201, r.status_code)

    def test_delete(self):
        visit_item = baker.make('studies.VisitItem', visit=self.visit1)
        obj = baker.make('studies.PatientVisit', study=self.study1, visit=self.visit1, patient=self.patient1)
        pvi = baker.prepare('studies.PatientVisitItem', patient_visit=obj, approved=None, visit_item=visit_item)
        pvi.approved = None
        pvi.save()

        self.do_auth_admin()
        r = self.client.delete(reverse('patientvisit-detail', args=(obj.id, )))
        self.assertEqual(204, r.status_code)

    def test_delete_failed_approved_true(self):
        visit_item = baker.make('studies.VisitItem', visit=self.visit1)
        obj = baker.make('studies.PatientVisit', study=self.study1, visit=self.visit1, patient=self.patient1)
        pvi = baker.prepare('studies.PatientVisitItem', patient_visit=obj, approved=None, visit_item=visit_item)
        pvi.approved = True
        pvi.save()

        self.do_auth_admin()
        r = self.client.delete(reverse('patientvisit-detail', args=(obj.id, )))
        self.assertEqual(400, r.status_code)

    def test_delete_failed_approved_false(self):
        visit_item = baker.make('studies.VisitItem', visit=self.visit1)
        obj = baker.make('studies.PatientVisit', study=self.study1, visit=self.visit1, patient=self.patient1)
        pvi = baker.prepare('studies.PatientVisitItem', patient_visit=obj, approved=None, visit_item=visit_item)
        pvi.approved = False
        pvi.save()

        self.do_auth_admin()
        r = self.client.delete(reverse('patientvisit-detail', args=(obj.id, )))
        self.assertEqual(204, r.status_code)
