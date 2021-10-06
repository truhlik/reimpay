from django.test import TestCase

from model_bakery import baker
from requests import Request

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER
from main.apps.studies.models import Visit, VisitItem
from main.apps.users import constants as user_constants

from ... import constants, utils
from ...constants import STUDY_VISIT_TYPE_UNSCHEDULED, STUDY_VISIT_TYPE_REGULAR, STUDY_VISIT_TYPE_DISCONTINUAL


class UtilsTestCase(TestCase):

    def setUp(self) -> None:
        super(UtilsTestCase, self).setUp()
        self.maxDiff = None

    def test_get_first_scheduled_visit_for_arm(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        utils.create_visits(study1, arm)
        first_visit = utils.get_first_scheduled_visit_for_arm(arm)
        self.assertIsNotNone(first_visit)
        self.assertEqual(first_visit.visit_type, constants.STUDY_VISIT_TYPE_REGULAR)

    def test_get_next_visit_from_visit_empty(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        utils.create_visits(study1, arm)
        visit = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        discontinual_visit = utils.get_next_visit_from_visit(visit)
        self.assertIsNotNone(discontinual_visit)
        self.assertEqual(constants.STUDY_VISIT_TYPE_DISCONTINUAL, discontinual_visit.visit_type)

    def test_get_next_visit_from_visit_regular(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        utils.create_visits(study1, arm)
        visit2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit3 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        v3 = utils.get_next_visit_from_visit(visit2)
        self.assertEqual(visit3, v3)

    def test_get_next_visit_from_visit_with_deleted(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        utils.create_visits(study1, arm)
        visit2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit3 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit3.deleted = True
        visit3.save()
        discontinual_visit = utils.get_next_visit_from_visit(visit2)
        self.assertIsNotNone(discontinual_visit)
        self.assertEqual(constants.STUDY_VISIT_TYPE_DISCONTINUAL, discontinual_visit.visit_type)

    def test_get_last_scheduled_visit_empty(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)

        visit = utils.get_last_scheduled_visit(patient)
        self.assertIsNone(visit)

    def test_get_last_scheduled_visit_one_regular_done(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        visit2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit3 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)

        baker.make('studies.PatientVisit', patient=patient, visit=visit2)

        visit = utils.get_last_scheduled_visit(patient)
        self.assertIsNotNone(visit)
        self.assertEqual(visit2, visit)

    def test_get_last_scheduled_visit_one_regular_done_and_uscheduled_done(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        visit2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit3 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)

        unscheduled_visit = Visit.objects.unscheduled().first()
        baker.make('studies.PatientVisit', patient=patient, visit=visit2)
        baker.make('studies.PatientVisit', patient=patient, visit=unscheduled_visit)

        visit = utils.get_last_scheduled_visit(patient)
        self.assertIsNotNone(visit)
        self.assertEqual(visit2, visit)

    def test_get_last_scheduled_visit_discontinual_done(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        visit2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit3 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)

        discontinual_visit = Visit.objects.discontinual().first()
        baker.make('studies.PatientVisit', patient=patient, visit=visit2)
        baker.make('studies.PatientVisit', patient=patient, visit=discontinual_visit)

        visit = utils.get_last_scheduled_visit(patient)
        self.assertIsNotNone(visit)
        self.assertEqual(discontinual_visit, visit)

    def test_filter_available_visit_items_empty_regular(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        vi_reg = baker.make('studies.VisitItem', study_item=study_item1, visit=regular)

        unscheduled = Visit.objects.unscheduled().first()
        vi_uns = baker.make('studies.VisitItem', study_item=study_item2, visit=unscheduled)

        discontinual = Visit.objects.discontinual().first()
        vi_dis = baker.make('studies.VisitItem', study_item=study_item3, visit=discontinual)

        qs = utils.filter_available_visit_items(VisitItem.objects.all(), patient.id, constants.STUDY_VISIT_TYPE_REGULAR)
        self.assertEqual(1, len(qs))
        self.assertEqual(vi_reg, qs[0])

    def test_filter_available_visit_items_empty_discontinual(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        vi_reg = baker.make('studies.VisitItem', study_item=study_item1, visit=regular)

        unscheduled = Visit.objects.unscheduled().first()
        vi_uns = baker.make('studies.VisitItem', study_item=study_item2, visit=unscheduled)

        discontinual = Visit.objects.discontinual().first()
        vi_dis = baker.make('studies.VisitItem', study_item=study_item3, visit=discontinual)

        qs = utils.filter_available_visit_items(VisitItem.objects.all(), patient.id, constants.STUDY_VISIT_TYPE_DISCONTINUAL)
        self.assertEqual(1, len(qs))
        self.assertEqual(vi_dis, qs[0])

    def test_filter_available_visit_items_empty_unscheduled(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        vi_reg = baker.make('studies.VisitItem', study_item=study_item1, visit=regular)

        unscheduled = Visit.objects.unscheduled().first()
        vi_uns = baker.make('studies.VisitItem', study_item=study_item2, visit=unscheduled)

        discontinual = Visit.objects.discontinual().first()
        vi_dis = baker.make('studies.VisitItem', study_item=study_item3, visit=discontinual)

        qs = utils.filter_available_visit_items(VisitItem.objects.all(), patient.id, constants.STUDY_VISIT_TYPE_UNSCHEDULED)
        self.assertEqual(1, len(qs))
        self.assertEqual(vi_uns, qs[0])

    def test_filter_available_visit_items_regular_filter_one_done(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        regular2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        vi_reg = baker.make('studies.VisitItem', study_item=study_item1, visit=regular2)

        unscheduled = Visit.objects.unscheduled().first()
        vi_uns = baker.make('studies.VisitItem', study_item=study_item2, visit=unscheduled)

        discontinual = Visit.objects.discontinual().first()
        vi_dis = baker.make('studies.VisitItem', study_item=study_item3, visit=discontinual)

        baker.make('studies.PatientVisit', patient=patient, visit=regular)

        qs = utils.filter_available_visit_items(VisitItem.objects.all(), patient.id, constants.STUDY_VISIT_TYPE_REGULAR)
        self.assertEqual(1, len(qs))
        self.assertEqual(vi_reg, qs[0])

    def test_filter_available_visit_items_next_only(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        regular2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        vi_reg = baker.make('studies.VisitItem', study_item=study_item1, visit=regular)

        unscheduled = Visit.objects.unscheduled().first()
        vi_uns = baker.make('studies.VisitItem', study_item=study_item2, visit=unscheduled)

        discontinual = Visit.objects.discontinual().first()
        vi_dis = baker.make('studies.VisitItem', study_item=study_item3, visit=discontinual)

        qs = utils.filter_available_visit_items(VisitItem.objects.all(), patient.id, next_only=True)
        self.assertEqual(3, len(qs))
        self.assertEqual(vi_reg, qs[0])

    def test_can_have_next_visit_without_visit(self):
        self.c1 = baker.make('companies.Company')
        self.user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.study1 = baker.make('studies.Study', company=self.c1)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        utils.create_visits(self.study1, self.arm1)
        self.site1 = baker.make('studies.Site', study=self.study1)
        patient1 = baker.make('studies.Patient', arm=self.arm1, site=self.site1, study=self.study1)
        self.assertTrue(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_REGULAR))

    def test_can_have_next_visit_with_already_one_unscheduled(self):
        self.c1 = baker.make('companies.Company')
        self.user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.study1 = baker.make('studies.Study', company=self.c1)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        utils.create_visits(self.study1, self.arm1)
        self.site1 = baker.make('studies.Site', study=self.study1)
        patient1 = baker.make('studies.Patient', arm=self.arm1, site=self.site1, study=self.study1)

        unscheduled = Visit.objects.unscheduled().first()
        baker.make('studies.PatientVisit', patient=patient1, visit=unscheduled)
        self.assertTrue(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_UNSCHEDULED))
        self.assertTrue(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_REGULAR))
        self.assertTrue(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_DISCONTINUAL))

    def test_can_have_next_visit_with_already_all_regular_done(self):
        self.c1 = baker.make('companies.Company')
        self.user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.study1 = baker.make('studies.Study', company=self.c1)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        utils.create_visits(self.study1, self.arm1)
        self.site1 = baker.make('studies.Site', study=self.study1)
        patient1 = baker.make('studies.Patient', arm=self.arm1, site=self.site1, study=self.study1)

        regular = Visit.objects.regular().first()
        baker.make('studies.PatientVisit', patient=patient1, visit=regular)
        self.assertFalse(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_REGULAR))
        self.assertTrue(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_DISCONTINUAL))
        self.assertTrue(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_UNSCHEDULED))

    def test_can_have_next_visit_with_already_discontinual_done(self):
        self.c1 = baker.make('companies.Company')
        self.user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.study1 = baker.make('studies.Study', company=self.c1)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        utils.create_visits(self.study1, self.arm1)
        self.site1 = baker.make('studies.Site', study=self.study1)
        patient1 = baker.make('studies.Patient', arm=self.arm1, site=self.site1, study=self.study1)

        discontinual = Visit.objects.discontinual().first()
        baker.make('studies.PatientVisit', patient=patient1, visit=discontinual)
        self.assertFalse(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_DISCONTINUAL))
        self.assertFalse(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_REGULAR))
        self.assertFalse(utils.can_have_next_visit(patient1, constants.STUDY_VISIT_TYPE_UNSCHEDULED))

    def test_filter_available_visit_empty_regular(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        unscheduled = Visit.objects.unscheduled().first()
        discontinual = Visit.objects.discontinual().first()

        qs = utils.filter_available_visits(Visit.objects.all(), patient.id, constants.STUDY_VISIT_TYPE_REGULAR)
        self.assertEqual(1, len(qs))
        self.assertEqual(regular, qs[0])

    def test_filter_available_visit_empty_discontinual(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        unscheduled = Visit.objects.unscheduled().first()
        discontinual = Visit.objects.discontinual().first()

        qs = utils.filter_available_visits(Visit.objects.all(), patient.id, constants.STUDY_VISIT_TYPE_DISCONTINUAL)
        self.assertEqual(1, len(qs))
        self.assertEqual(discontinual, qs[0])

    def test_filter_available_visit_empty_unscheduled(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        unscheduled = Visit.objects.unscheduled().first()
        discontinual = Visit.objects.discontinual().first()

        qs = utils.filter_available_visits(Visit.objects.all(), patient.id, constants.STUDY_VISIT_TYPE_UNSCHEDULED)
        self.assertEqual(1, len(qs))
        self.assertEqual(unscheduled, qs[0])

    def test_filter_available_visit_regular_filter_one_done(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        regular2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        unscheduled = Visit.objects.unscheduled().first()
        discontinual = Visit.objects.discontinual().first()

        baker.make('studies.PatientVisit', patient=patient, visit=regular)

        qs = utils.filter_available_visits(Visit.objects.all(), patient.id, constants.STUDY_VISIT_TYPE_REGULAR)
        self.assertEqual(1, len(qs))
        self.assertEqual(regular2, qs[0])

    def test_filter_available_visit_next_only(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        regular2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        unscheduled = Visit.objects.unscheduled().first()
        discontinual = Visit.objects.discontinual().first()

        qs = utils.filter_available_visits(Visit.objects.all(), patient.id, next_only=True)
        self.assertEqual(3, len(qs))
        self.assertEqual(regular, qs[0])

    def test_filter_available_visit_discontinual_done(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study_item1 = baker.make('studies.StudyItem')
        study_item2 = baker.make('studies.StudyItem')
        study_item3 = baker.make('studies.StudyItem')

        site = baker.make('studies.Site', study=study1)
        arm = baker.make('studies.Arm', study=study1)
        patient = baker.make('studies.Patient', site=site, arm=arm)

        utils.create_visits(study1, arm)
        regular = Visit.objects.regular().first()
        regular2 = baker.make('studies.Visit', arm=arm, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        unscheduled = Visit.objects.unscheduled().first()
        discontinual = Visit.objects.discontinual().first()

        baker.make('studies.PatientVisit', patient=patient, visit=discontinual)

        qs = utils.filter_available_visits(Visit.objects.all(), patient.id, next_only=True)
        self.assertEqual(0, len(qs))

    def test_get_unscheduled_visits(self):
        patient = baker.make('studies.Patient')
        visit = baker.make('studies.Visit', arm=patient.arm, visit_type=constants.STUDY_VISIT_TYPE_UNSCHEDULED)
        pv = baker.make('studies.PatientVisit', patient=patient, visit=visit)
        qs = utils.get_unscheduled_visits(patient)
        self.assertEqual(1, len(qs))
        self.assertEqual(pv, qs[0])

    def test_get_expected_patients(self):
        study1 = baker.make('studies.Study')
        baker.make('studies.Site', study=study1, expected_patients=10)
        baker.make('studies.Site', study=study1, expected_patients=20)
        baker.make('studies.Site', study=study1, expected_patients=30)
        self.assertEqual(60, utils.get_expected_patients(study1))

    def test_get_expected_patients_empty(self):
        study1 = baker.make('studies.Study')
        self.assertEqual(0, utils.get_expected_patients(study1))

    def test_get_study_patients(self):
        study1 = baker.make('studies.Study')
        baker.make('studies.Patient', study=study1)
        baker.make('studies.Patient', study=study1)
        baker.make('studies.Patient', study=study1)
        self.assertEqual(3, utils.get_study_patients(study=study1))

    def test_get_study_patients_empty(self):
        study1 = baker.make('studies.Study')
        self.assertEqual(0, utils.get_study_patients(study=study1))

    def test_get_avg_visits_for_study(self):
        study1 = baker.make('studies.Study')
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study1)
        baker.make('studies.Visit', arm=arm1)
        baker.make('studies.Visit', arm=arm1)
        baker.make('studies.Visit', arm=arm1)
        baker.make('studies.Visit', arm=arm2)
        self.assertEqual(2, utils.get_avg_visits_for_study(study1))

    def test_get_remaining_visits(self):
        study1 = baker.make('studies.Study')
        baker.make('studies.Site', study=study1, expected_patients=10)
        baker.make('studies.Site', study=study1, expected_patients=20)
        baker.make('studies.Site', study=study1, expected_patients=30)
        baker.make('studies.Patient', study=study1)
        baker.make('studies.Patient', study=study1)
        baker.make('studies.Patient', study=study1)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study1)
        baker.make('studies.Visit', arm=arm1)
        baker.make('studies.Visit', arm=arm1)
        baker.make('studies.Visit', arm=arm1)
        baker.make('studies.Visit', arm=arm2)
        self.assertEqual(120, utils.get_remaining_visits(study1))

    def test_get_remaining_visits_with_less_expected(self):
        study1 = baker.make('studies.Study')
        baker.make('studies.Site', study=study1, expected_patients=1)
        baker.make('studies.Site', study=study1, expected_patients=0)
        baker.make('studies.Site', study=study1, expected_patients=0)
        baker.make('studies.Patient', study=study1)
        baker.make('studies.Patient', study=study1)
        baker.make('studies.Patient', study=study1)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study1)
        baker.make('studies.Visit', arm=arm1)
        baker.make('studies.Visit', arm=arm1)
        baker.make('studies.Visit', arm=arm1)
        baker.make('studies.Visit', arm=arm2)
        self.assertEqual(6, utils.get_remaining_visits(study1))

    def test_get_avg_visit_value(self):
        study1 = baker.make('studies.Study')
        baker.make('studies.PatientVisitItem', patient_visit__study=study1, visit_item__study_item__price=100)
        baker.make('studies.PatientVisitItem', patient_visit__study=study1, visit_item__study_item__price=200)
        baker.make('studies.PatientVisitItem', patient_visit__study=study1, visit_item__study_item__price=300)
        self.assertEqual(200, utils.get_avg_visit_value(study1))

    def test_generate_variable_symbol(self):
        vs = utils.generate_variable_symbol()
        self.assertLess(vs, 10000000000)
        self.assertGreater(vs, 999999999)

    def test_create_stats(self):
        study1 = baker.make('studies.Study')

        site1 = baker.make('studies.Site', study=study1, title='site1')
        site2 = baker.make('studies.Site', study=study1, title='site2')

        arm1 = baker.make('studies.Arm', study=study1, title='arm1')
        arm2 = baker.make('studies.Arm', study=study1, title='arm2')

        p1 = baker.make('studies.Patient', study=study1, site=site1, arm=arm1, number='P1')
        p2 = baker.make('studies.Patient', study=study1, site=site1, arm=arm1, number='P2')
        p3 = baker.make('studies.Patient', study=study1, site=site1, arm=arm2, number='P3')
        p4 = baker.make('studies.Patient', study=study1, site=site2, arm=arm1, number='P4')

        p1_url = 'http://example.com/app/#/patient/{}/'.format(p1.id)
        p2_url = 'http://example.com/app/#/patient/{}/'.format(p2.id)
        p3_url = 'http://example.com/app/#/patient/{}/'.format(p3.id)
        p4_url = 'http://example.com/app/#/patient/{}/'.format(p4.id)

        v1 = baker.make('studies.Visit', arm=arm1, study=study1, title='prvni arm 1', order=1)
        v2 = baker.make('studies.Visit', arm=arm1, study=study1, title='druha arm 1', order=2)
        v3 = baker.make('studies.Visit', arm=arm1, study=study1, title='treti arm 1', order=3)
        v4 = baker.make('studies.Visit', arm=arm2, study=study1, title='prvni arm 2', order=1)
        v5 = baker.make('studies.Visit', arm=arm2, study=study1, title='druha arm 2', order=2)

        baker.make('studies.PatientVisit', patient=p2, visit=v2, study=study1)

        baker.make('studies.PatientVisitItem', patient_visit__patient=p1, patient_visit__visit=v1, approved=True, visit_item__study_item__price=1)
        baker.make('studies.PatientVisitItem', patient_visit__patient=p1, patient_visit__visit=v1, approved=True, visit_item__study_item__price=1)
        baker.make('studies.PatientVisitItem', patient_visit__patient=p1, patient_visit__visit=v2, approved=True, visit_item__study_item__price=1)
        baker.make('studies.PatientVisitItem', patient_visit__patient=p1, patient_visit__visit=v3, approved=True, visit_item__study_item__price=1)
        baker.make('studies.PatientVisitItem', patient_visit__patient=p2, patient_visit__visit=v1, approved=True, visit_item__study_item__price=1)
        baker.make('studies.PatientVisitItem', patient_visit__patient=p3, patient_visit__visit=v4, approved=True, visit_item__study_item__price=1)
        baker.make('studies.PatientVisitItem', patient_visit__patient=p4, patient_visit__visit=v1, approved=True, visit_item__study_item__price=1)
        baker.make('studies.PatientVisitItem', patient_visit__patient=p4, patient_visit__visit=v3, approved=True, visit_item__study_item__price=1)

        dct = utils.create_stats(study1)

        exp_dct = {
            'site1': {
                'arm1': [
                    {'Patient': ['Add visit', 'prvni arm 1', 'druha arm 1', 'treti arm 1', 'Total']},
                    {'P1': [p1_url, 2, 1, 1, 4]},
                    {'P2': [p2_url, 1, 0, "-", 1]}
                ],
                'arm2': [
                    {'Patient': ['Add visit', 'prvni arm 2', 'druha arm 2', 'Total']},
                    {'P3': [p3_url, 1, "-", 1]}
                ]
            },
            'site2': {
                'arm1': [
                    {'Patient': ['Add visit', 'prvni arm 1', 'druha arm 1', 'treti arm 1', 'Total']},
                    {'P4': [p4_url, 1, "-", 1, 2]}
                ]}
        }
        self.assertEqual(exp_dct, dct)

    def test_can_delete_patient_visit_false(self):
        study = baker.make('studies.Study')
        visit1 = baker.make('studies.Visit')
        visit_item = baker.make('studies.VisitItem', visit=visit1)
        obj = baker.make('studies.PatientVisit', study=study, visit=visit1)
        pvi = baker.prepare('studies.PatientVisitItem', patient_visit=obj, approved=None, visit_item=visit_item)
        pvi.approved = False
        pvi.save()
        self.assertTrue(utils.can_delete_patient_visit(obj))

    def test_can_delete_patient_visit_true(self):
        study = baker.make('studies.Study')
        visit1 = baker.make('studies.Visit')
        visit_item = baker.make('studies.VisitItem', visit=visit1)
        obj = baker.make('studies.PatientVisit', study=study, visit=visit1)
        pvi = baker.prepare('studies.PatientVisitItem', patient_visit=obj, approved=None, visit_item=visit_item)
        pvi.approved = True
        pvi.save()
        self.assertFalse(utils.can_delete_patient_visit(obj))

    def test_can_delete_patient_visit_none(self):
        study = baker.make('studies.Study')
        visit1 = baker.make('studies.Visit')
        visit_item = baker.make('studies.VisitItem', visit=visit1)
        obj = baker.make('studies.PatientVisit', study=study, visit=visit1)
        pvi = baker.prepare('studies.PatientVisitItem', patient_visit=obj, approved=None, visit_item=visit_item)
        pvi.approved = None
        pvi.save()
        self.assertTrue(utils.can_delete_patient_visit(obj))


class VisitItemUtilsTestCase(TestCase):

    def test_get_visit_item_cost(self):
        study_item = baker.make('studies.StudyItem', price=100)
        visit1 = baker.make('studies.Visit', visit_type=STUDY_VISIT_TYPE_REGULAR, study=study_item.study)
        visit2 = baker.make('studies.Visit', visit_type=STUDY_VISIT_TYPE_UNSCHEDULED, study=study_item.study)
        visit3 = baker.make('studies.Visit', visit_type=STUDY_VISIT_TYPE_DISCONTINUAL, study=study_item.study)

        v1 = baker.make('studies.VisitItem', study_item=study_item, study=study_item.study, visit=visit1)
        v2 = baker.make('studies.VisitItem', study_item=study_item, study=study_item.study, visit=visit1)
        v3 = baker.make('studies.VisitItem', study_item=study_item, study=study_item.study, visit=visit2)
        v4 = baker.make('studies.VisitItem', study_item=study_item, study=study_item.study, visit=visit3)

        value = utils.get_visit_item_cost(v1.visit.arm)
        self.assertEqual(200, value)
