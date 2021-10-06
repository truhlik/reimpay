from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from .. import BaseViewPermissionTestCase

from .... import constants
from ....utils import PAYMENT_TYPE_BANK_TRANSFER


class DoctorPatchTestCase(BaseViewPermissionTestCase):

    def setUp(self) -> None:
        super(DoctorPatchTestCase, self).setUp()

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
            'payment_info': '7998862/0800',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'number': self.patient1.number,
            'name': '',
            'street': '',
            'street_number': '',
            'city': '',
            'zip': '',
        }

        self.patient_visit_data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
        }

        self.patient_visit_item_data = {
            'visit_item': self.visit_item.id,
            'patient_visit': self.patient_visit.id,
        }

    def test_patch_draft(self):

        self.study1.status = constants.STUDY_STATUS_DRAFT
        self.study1.save()

        self.assertEqual(401, self.client.patch(reverse('study-detail', args=(self.study1.id, )), data=self.study_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('studyitem-detail', args=(self.study_item1.id, )), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('arm-detail', args=(self.arm1.id, )), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('site-detail', args=(self.site1.id, )), data=self.site_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visit-detail', args=(self.visit1.id, )), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visititem-detail', args=(self.visit_item.id, )), data=self.visit_item_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('patient-detail', args=(self.patient1.id, )), data=self.patient_data).status_code)
        # self.assertEqual(400, self.client.patch(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('patientvisititem-detail', args=(self.pvi.id, )), data=self.patient_visit_item_data).status_code)

    def test_patch_prelaunch(self):
        self.study1.status = constants.STUDY_STATUS_PRELAUNCH
        self.study1.save()

        self.assertEqual(401, self.client.patch(reverse('study-detail', args=(self.study1.id, )), data=self.study_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('studyitem-detail', args=(self.study_item1.id, )), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('arm-detail', args=(self.arm1.id, )), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('site-detail', args=(self.site1.id, )), data=self.site_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visit-detail', args=(self.visit1.id, )), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visititem-detail', args=(self.visit_item.id, )), data=self.visit_item_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('patient-detail', args=(self.patient1.id,)), data=self.patient_data).status_code)
        # self.assertEqual(401, self.client.patch(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('patientvisititem-detail', args=(self.pvi.id, )), data=self.patient_visit_item_data).status_code)

    def test_patch_progress(self):
        self.study1.status = constants.STUDY_STATUS_PROGRESS
        self.study1.save()

        self.assertEqual(401, self.client.patch(reverse('study-detail', args=(self.study1.id, )), data=self.study_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('studyitem-detail', args=(self.study_item1.id, )), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('arm-detail', args=(self.arm1.id, )), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('site-detail', args=(self.site1.id, )), data=self.site_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visit-detail', args=(self.visit1.id, )), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visititem-detail', args=(self.visit_item.id, )), data=self.visit_item_data).status_code)
        self.assertEqual(200, self.client.patch(reverse('patient-detail', args=(self.patient1.id,)), data=self.patient_data).status_code)
        # self.assertEqual(400, self.client.patch(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('patientvisititem-detail', args=(self.pvi.id, )), data=self.patient_visit_item_data).status_code)

    def test_patch_billing(self):
        self.study1.status = constants.STUDY_STATUS_BILLING
        self.study1.save()

        self.assertEqual(401, self.client.patch(reverse('study-detail', args=(self.study1.id, )), data=self.study_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('studyitem-detail', args=(self.study_item1.id, )), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('arm-detail', args=(self.arm1.id, )), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('site-detail', args=(self.site1.id, )), data=self.site_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visit-detail', args=(self.visit1.id, )), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visititem-detail', args=(self.visit_item.id, )), data=self.visit_item_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('patient-detail', args=(self.patient1.id,)), data=self.patient_data).status_code)
        # self.assertEqual(401, self.client.patch(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('patientvisititem-detail', args=(self.pvi.id, )), data=self.patient_visit_item_data).status_code)

    def test_patch_closed(self):
        self.study1.status = constants.STUDY_STATUS_CLOSED
        self.study1.save()

        self.assertEqual(401, self.client.patch(reverse('study-detail', args=(self.study1.id, )), data=self.study_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('studyitem-detail', args=(self.study_item1.id, )), data=self.study_item_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('arm-detail', args=(self.arm1.id, )), data=self.arm_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('site-detail', args=(self.site1.id, )), data=self.site_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visit-detail', args=(self.visit1.id, )), data=self.visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('visititem-detail', args=(self.visit_item.id, )), data=self.visit_item_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('patient-detail', args=(self.patient1.id,)), data=self.patient_data).status_code)
        # self.assertEqual(401, self.client.patch(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.patch(reverse('patientvisititem-detail', args=(self.pvi.id, )), data=self.patient_visit_item_data).status_code)
