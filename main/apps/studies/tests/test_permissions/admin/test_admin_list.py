from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER
from main.apps.users import constants as user_constatnts
from .. import BaseViewPermissionTestCase

from ....models import VisitItem, PatientVisit, PatientVisitItem
from .... import constants


class AdminListTestCase(BaseViewPermissionTestCase):

    def setUp(self) -> None:
        super(AdminListTestCase, self).setUp()

        self.client.force_authenticate(user=self.user_admin)

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

        self.patient_visit_data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
        }

        self.patient_visit_item_data = {
            'visit_item': self.visit_item.id,
            'patient_visit': self.patient_visit.id,
        }

    def test_list_draft(self):

        self.study1.status = constants.STUDY_STATUS_DRAFT
        self.study1.save()

        self.assertEqual(200, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

    def test_list_prelaunch(self):
        self.study1.status = constants.STUDY_STATUS_PRELAUNCH
        self.study1.save()

        self.assertEqual(200, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

    def test_list_progress(self):
        self.study1.status = constants.STUDY_STATUS_PROGRESS
        self.study1.save()

        self.assertEqual(200, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

    def test_list_billing(self):
        self.study1.status = constants.STUDY_STATUS_BILLING
        self.study1.save()

        self.assertEqual(200, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

    def test_list_closed(self):
        self.study1.status = constants.STUDY_STATUS_CLOSED
        self.study1.save()

        self.assertEqual(200, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

