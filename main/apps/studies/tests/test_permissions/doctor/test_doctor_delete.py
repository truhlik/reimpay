from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .. import BaseViewPermissionTestCase

from .... import constants


class DoctorDeleteTestCase(BaseViewPermissionTestCase):

    def setUp(self) -> None:
        super(DoctorDeleteTestCase, self).setUp()
        # uložím do session login informace doktora
        session = self.client.session
        session[settings.DOCTOR_SESSION_KEY] = {
            self.patient1.id: (timezone.now() + timezone.timedelta(minutes=30)).isoformat()
        }
        session.save()

    def test_delete_draft(self):

        self.study1.status = constants.STUDY_STATUS_DRAFT
        self.study1.save()

        self.assertEqual(401, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, ))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('study-detail', args=(self.study1.id, ))).status_code)

    def test_delete_prelaunch(self):
        self.study1.status = constants.STUDY_STATUS_PRELAUNCH
        self.study1.save()

        self.assertEqual(401, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, ))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('study-detail', args=(self.study1.id,))).status_code)

    def test_delete_progress(self):
        self.study1.status = constants.STUDY_STATUS_PROGRESS
        self.study1.save()

        self.assertEqual(401, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, ))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('study-detail', args=(self.study1.id,))).status_code)

    def test_delete_billing(self):
        self.study1.status = constants.STUDY_STATUS_BILLING
        self.study1.save()

        self.assertEqual(401, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, ))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('study-detail', args=(self.study1.id,))).status_code)

    def test_delete_closed(self):
        self.study1.status = constants.STUDY_STATUS_CLOSED
        self.study1.save()

        self.assertEqual(401, self.client.delete(reverse('patientvisititem-detail', args=(self.pvi.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patientvisit-detail', args=(self.patient_visit.id, ))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visititem-detail', args=(self.visit_item.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('visit-detail', args=(self.visit1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('patient-detail', args=(self.patient1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('site-detail', args=(self.site1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('arm-detail', args=(self.arm1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('studyitem-detail', args=(self.study_item1.id,))).status_code)
        self.assertEqual(401, self.client.delete(reverse('study-detail', args=(self.study1.id,))).status_code)
