from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from .. import BaseViewPermissionTestCase

from .... import constants


class DoctoListTestCase(BaseViewPermissionTestCase):

    def setUp(self) -> None:
        super(DoctoListTestCase, self).setUp()

        # uložím do session login informace doktora
        session = self.client.session
        session[settings.DOCTOR_SESSION_KEY] = {
            self.patient1.id: (timezone.now() + timezone.timedelta(minutes=30)).isoformat()
        }
        session.save()

    def test_list_draft(self):

        self.study1.status = constants.STUDY_STATUS_DRAFT
        self.study1.save()

        self.assertEqual(401, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

    def test_list_prelaunch(self):
        self.study1.status = constants.STUDY_STATUS_PRELAUNCH
        self.study1.save()

        self.assertEqual(401, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

    def test_list_progress(self):
        self.study1.status = constants.STUDY_STATUS_PROGRESS
        self.study1.save()

        self.assertEqual(401, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

    def test_list_billing(self):
        self.study1.status = constants.STUDY_STATUS_BILLING
        self.study1.save()

        self.assertEqual(401, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

    def test_list_closed(self):
        self.study1.status = constants.STUDY_STATUS_CLOSED
        self.study1.save()

        self.assertEqual(401, self.client.get(reverse('study-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('studyitem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('arm-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('site-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visit-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('visititem-list')).status_code)
        self.assertEqual(401, self.client.get(reverse('patient-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisit-list')).status_code)
        self.assertEqual(200, self.client.get(reverse('patientvisititem-list')).status_code)

