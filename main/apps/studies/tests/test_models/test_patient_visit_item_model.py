from django.test import TestCase
from mock import patch

from model_bakery import baker

from main.apps.users import constants as user_constants

from ... import constants


class PatientVisitItemModelTestCase(TestCase):

    def setUp(self) -> None:
        super(PatientVisitItemModelTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.study1 = baker.make('studies.Study', company=self.c1, status=constants.STUDY_STATUS_BILLING)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        self.site1 = baker.make('studies.Site', study=self.study1)
        self.patient = baker.make('studies.Patient', arm=self.arm1, site=self.site1, study=self.study1)
        self.visit1 = baker.make('studies.Visit', study=self.study1, arm=self.arm1)
        self.study_item1 = baker.make('studies.StudyItem', study=self.study1)
        self.visit_item = baker.make('studies.VisitItem', study_item=self.study_item1, visit=self.visit1, study=self.study1)
        self.pv1 = baker.make('studies.PatientVisit', patient=self.patient, visit=self.visit1, study=self.study1)
        self.obj1 = baker.make('studies.PatientVisitItem', patient_visit=self.pv1, visit_item=self.visit_item)

    def test_is_owner_admin_associated_with_this_study(self):
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.assertTrue(self.obj1.is_owner(user))

    def test_is_owner_cra_associated_with_this_study(self):
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=self.c1)
        self.site1.cra = user
        self.site1.save()
        self.assertTrue(self.obj1.is_owner(user))

    def test_is_owner_admin_from_other_company(self):
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c2)
        self.assertFalse(self.obj1.is_owner(user))

    def test_status_without_approval(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=None)
        self.assertEqual('WAITING FOR CRA APPROVAL', obj1.status)

    def test_status_without_rejected(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=False)
        self.assertEqual('REJECTED', obj1.status)

    def test_status_with_approved(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=True,
                          payment_status=constants.STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_WAITING)
        self.assertEqual('In enque for processing', obj1.status)

    def test_approved_was_changed(self):
        obj1 = baker.prepare('studies.PatientVisitItem', approved=None)
        self.assertFalse(obj1.approved_was_changed())

    def test_approved_was_changed_create_with_false(self):
        obj1 = baker.prepare('studies.PatientVisitItem', approved=False)
        self.assertFalse(obj1.approved_was_changed())

    def test_approved_was_changed_create_with_true(self):
        obj1 = baker.prepare('studies.PatientVisitItem', approved=True)
        self.assertFalse(obj1.approved_was_changed())

    def test_approved_was_changed_edit_to_true(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=None)
        obj1.approved = True
        self.assertTrue(obj1.approved_was_changed())

    def test_approved_was_changed_edit_false(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=None)
        obj1.approved = False
        self.assertTrue(obj1.approved_was_changed())

    def test_approved_was_changed_edit_false_to_false(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=False)
        obj1.approved = False
        self.assertFalse(obj1.approved_was_changed())

    def test_approved_was_changed_edit_true_to_true(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=True)
        obj1.approved = True
        self.assertFalse(obj1.approved_was_changed())

    def test_should_send_approved_signal_create_with_none(self):
        obj1 = baker.prepare('studies.PatientVisitItem', approved=None)
        self.assertFalse(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_create_with_false(self):
        obj1 = baker.prepare('studies.PatientVisitItem', approved=False)
        self.assertFalse(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_create_with_true(self):
        obj1 = baker.prepare('studies.PatientVisitItem', approved=True)
        self.assertTrue(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_edit_to_none(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=True)
        obj1.approved = None
        self.assertFalse(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_edit_to_false(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=True)
        obj1.approved = False
        self.assertFalse(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_edit_to_true(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=True)
        obj1.approved = True
        self.assertFalse(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_edit_to_none_from_none(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=None)
        obj1.approved = None
        self.assertFalse(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_edit_to_false_from_none(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=None)
        obj1.approved = False
        self.assertFalse(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_edit_to_true_from_none(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=None)
        obj1.approved = True
        self.assertTrue(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_edit_to_none_from_false(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=False)
        obj1.approved = None
        self.assertFalse(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_edit_to_false_from_false(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=False)
        obj1.approved = False
        self.assertFalse(obj1.should_send_approved_signal())

    def test_should_send_approved_signal_edit_to_true_from_false(self):
        obj1 = baker.make('studies.PatientVisitItem', approved=False)
        obj1.approved = True
        self.assertTrue(obj1.should_send_approved_signal())

    @patch('main.apps.studies.signals.approved.send')
    def test_send_signal(self, mock_send):
        study = baker.make('studies.Study', commission=10)
        si = baker.make('studies.StudyItem', price=100, study=study)
        vi = baker.make('studies.VisitItem', study_item=si, study=study)
        pv = baker.make('studies.PatientVisit', study=study)
        pvi = baker.prepare('studies.PatientVisitItem', patient_visit=pv, visit_item=vi)
        pvi.approved = True
        pvi.save()
        self.assertTrue(mock_send.called)
