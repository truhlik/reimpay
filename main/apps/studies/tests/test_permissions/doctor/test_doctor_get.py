from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from .. import BaseViewPermissionTestCase
from .... import constants


class DoctorGetTestCase(BaseViewPermissionTestCase):

    def setUp(self) -> None:
        super(DoctorGetTestCase, self).setUp()

        # uložím do session login informace doktora
        session = self.client.session
        session[settings.DOCTOR_SESSION_KEY] = {
            self.patient1.id: (timezone.now() + timezone.timedelta(minutes=30)).isoformat()
        }
        session.save()

    def test_get_draft(self):

        self.study1.status = constants.STUDY_STATUS_DRAFT
        self.study1.save()

        self.assertEqual(405, self.client.get(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        # self.assertEqual(404, self.client.get(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('study-detail', args=(self.study1.id, ))).status_code)

    def test_get_prelaunch(self):
        self.study1.status = constants.STUDY_STATUS_PRELAUNCH
        self.study1.save()

        self.assertEqual(405, self.client.get(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        # self.assertEqual(401, self.client.get(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('study-detail', args=(self.study1.id,))).status_code)

    def test_get_progress(self):
        self.study1.status = constants.STUDY_STATUS_PROGRESS
        self.study1.save()

        self.assertEqual(405, self.client.get(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        # self.assertEqual(401, self.client.get(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('study-detail', args=(self.study1.id,))).status_code)

    def test_get_billing(self):
        self.study1.status = constants.STUDY_STATUS_BILLING
        self.study1.save()

        self.assertEqual(405, self.client.get(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        # self.assertEqual(401, self.client.get(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('study-detail', args=(self.study1.id,))).status_code)

    def test_get_closed(self):
        self.study1.status = constants.STUDY_STATUS_CLOSED
        self.study1.save()

        self.assertEqual(405, self.client.get(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        # self.assertEqual(401, self.client.get(reverse('patientvisit-detail', args=(self.patient_visit.id, )), data=self.patient_visit_data).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(200, self.client.get(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.get(reverse('study-detail', args=(self.study1.id,))).status_code)
