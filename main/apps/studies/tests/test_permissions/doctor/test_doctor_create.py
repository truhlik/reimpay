from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER
from .. import BaseViewPermissionTestCase

from .... import constants


class DoctorCreateTestCase(BaseViewPermissionTestCase):

    def setUp(self) -> None:
        super(DoctorCreateTestCase, self).setUp()

        # uložím do session login informace doktora
        session = self.client.session
        session[settings.DOCTOR_SESSION_KEY] = {
            self.patient1.id: (timezone.now() + timezone.timedelta(minutes=30)).isoformat()
        }
        session.save()

        self.study_data = {
            'number': 1,
            'identifier': 'test22',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': True,
            'pay_frequency': 2,
        }
        self.study_item_data = {
            'title': 'test',
            'description': 'test',
            'price': 100,
            'study': str(self.study1.id),
        }

        self.arm_data = {
            'title': 'test',
            'max_unscheduled': 100,
            'study': str(self.study1.id),
        }

        self.site_data = {
            'title': 'test',
            'expected_patients': 100,
            'study': str(self.study1.id),
            'cra': self.user_cra.id,
        }

        self.visit_data = {
            'arm': self.arm1.id,
            'title': 'test',
        }

        self.visit_item_data = {
            'visit': self.visit1.id,
            'study_item': self.study_item1.id,
        }

        self.patient_data = {
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': 'test',
            'arm': self.arm1.id,
            'site': self.site1.id,
        }

        self.patient_visit_data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_DISCONTINUAL,
            'visit_date': timezone.now().date(),
        }

        self.patient_visit_item_data = {
            'visit_item': self.visit_item.id,
            'patient_visit': self.patient_visit.id,
        }

    def test_create_draft(self):

        self.study1.status = constants.STUDY_STATUS_DRAFT
        self.study1.save()

        self.assertEqual(401, self.client.post(reverse('study-list'), data=self.study_data).status_code)
        self.assertEqual(401, self.client.post(reverse('studyitem-list'), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('arm-list'), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.post(reverse('site-list'), data=self.site_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visit-list'), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visititem-list'), data=self.visit_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('patient-list'), data=self.patient_data).status_code)
        self.assertEqual(400, self.client.post(reverse('patientvisit-list'), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.post(reverse('patientvisititem-list'), data=self.patient_visit_item_data).status_code)

    def test_create_prelaunch(self):
        self.study1.status = constants.STUDY_STATUS_PRELAUNCH
        self.study1.save()

        self.assertEqual(401, self.client.post(reverse('study-list'), data=self.study_data).status_code)
        self.assertEqual(401, self.client.post(reverse('studyitem-list'), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('arm-list'), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.post(reverse('site-list'), data=self.site_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visit-list'), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visititem-list'), data=self.visit_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('patient-list'), data=self.patient_data).status_code)
        self.assertEqual(400, self.client.post(reverse('patientvisit-list'), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.post(reverse('patientvisititem-list'), data=self.patient_visit_item_data).status_code)

    def test_create_progress(self):
        self.study1.status = constants.STUDY_STATUS_PROGRESS
        self.study1.save()

        self.assertEqual(401, self.client.post(reverse('study-list'), data=self.study_data).status_code)
        self.assertEqual(401, self.client.post(reverse('studyitem-list'), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('arm-list'), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.post(reverse('site-list'), data=self.site_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visit-list'), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visititem-list'), data=self.visit_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('patient-list'), data=self.patient_data).status_code)
        self.assertEqual(201, self.client.post(reverse('patientvisit-list'), data=self.patient_visit_data).status_code)
        # r = self.client.post(reverse('patientvisit-list'), data=self.patient_visit_data)
        self.assertEqual(401, self.client.post(reverse('patientvisititem-list'), data=self.patient_visit_item_data).status_code)

    def test_create_billing(self):
        self.study1.status = constants.STUDY_STATUS_BILLING
        self.study1.save()

        self.assertEqual(401, self.client.post(reverse('study-list'), data=self.study_data).status_code)
        self.assertEqual(401, self.client.post(reverse('studyitem-list'), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('arm-list'), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.post(reverse('site-list'), data=self.site_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visit-list'), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visititem-list'), data=self.visit_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('patient-list'), data=self.patient_data).status_code)
        self.assertEqual(400, self.client.post(reverse('patientvisit-list'), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.post(reverse('patientvisititem-list'), data=self.patient_visit_item_data).status_code)

    def test_create_closed(self):
        self.study1.status = constants.STUDY_STATUS_CLOSED
        self.study1.save()

        self.assertEqual(401, self.client.post(reverse('study-list'), data=self.study_data).status_code)
        self.assertEqual(401, self.client.post(reverse('studyitem-list'), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('arm-list'), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.post(reverse('site-list'), data=self.site_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visit-list'), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.post(reverse('visititem-list'), data=self.visit_item_data).status_code)
        self.assertEqual(401, self.client.post(reverse('patient-list'), data=self.patient_data).status_code)
        self.assertEqual(400, self.client.post(reverse('patientvisit-list'), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.post(reverse('patientvisititem-list'), data=self.patient_visit_item_data).status_code)
