from django.urls import reverse
from django.utils import timezone

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER
from .. import BaseViewPermissionTestCase

from .... import constants


class CraDeleteTestCase(BaseViewPermissionTestCase):

    def setUp(self) -> None:
        super(CraDeleteTestCase, self).setUp()

        self.client.force_authenticate(user=self.user_cra)

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

        self.patient_data = {
            'payment_info': '123457890',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'number': self.patient1.number,
            'name': None,
            'street': None,
            'street_number': None,
            'city': None,
            'zip': None,
        }

        self.visit_data = {
            'arm': self.arm1.id,
            'title': 'test',
        }

        self.visit_item_data = {
            'visit': self.visit1.id,
            'study_item': self.study_item1.id,
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

    def test_delete_draft(self):

        self.study1.status = constants.STUDY_STATUS_DRAFT
        self.study1.save()

        self.assertEqual(405, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        self.assertEqual(204, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(403, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(405, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('study-detail', args=(self.study1.id, ))).status_code)

    def test_delete_prelaunch(self):
        self.study1.status = constants.STUDY_STATUS_PRELAUNCH
        self.study1.save()

        self.assertEqual(405, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(403, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(405, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('study-detail', args=(self.study1.id,))).status_code)

    def test_delete_progress(self):
        self.study1.status = constants.STUDY_STATUS_PROGRESS
        self.study1.save()

        self.assertEqual(405, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        self.assertEqual(204, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(403, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(405, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('study-detail', args=(self.study1.id,))).status_code)

    def test_delete_billing(self):
        self.study1.status = constants.STUDY_STATUS_BILLING
        self.study1.save()

        self.assertEqual(405, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(403, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(405, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('study-detail', args=(self.study1.id,))).status_code)

    def test_delete_closed(self):
        self.study1.status = constants.STUDY_STATUS_CLOSED
        self.study1.save()

        self.assertEqual(405, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        # self.assertEqual(403, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(403, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(405, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(403, self.client.delete(reverse('study-detail', args=(self.study1.id,))).status_code)
