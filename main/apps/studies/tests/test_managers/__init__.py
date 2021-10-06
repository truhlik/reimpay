from django.test import TestCase
from django.utils import timezone

from model_bakery import baker

from main.apps.studies.models import Visit, VisitItem, PatientVisit, PatientVisitItem
from main.apps.users import constants as user_constants

from ...models import Study, StudyItem, Patient
from ... import constants, utils


class StudyManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(StudyManagerTestCase, self).setUp()

    def test_owner_admin(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')
        qs = Study.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(study1.id, qs[0].id)

    def test_owner_cra(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study', company=c)
        qs = Study.objects.owner(user)
        self.assertEqual(0, len(qs))

    def test_company(self):
        c1 = baker.make('companies.Company')
        user = baker.make('users.User', company=c1)
        study1 = baker.make('studies.Study', company=c1)
        _ = baker.make('studies.Study')
        qs = Study.objects.company(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(study1.id, qs[0].id)

    def test_active(self):
        _ = baker.make('studies.Study', closed_at=timezone.now() - timezone.timedelta(days=1))
        study1 = baker.make('studies.Study', closed_at=timezone.now() + timezone.timedelta(days=1))
        study2 = baker.make('studies.Study', closed_at=None)
        qs = Study.objects.active().order_by('created_at')
        self.assertEqual(2, len(qs))
        self.assertEqual([study1.id, study2.id], [qs[0].id, qs[1].id])

    def test_list(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        baker.make('studies.Site', cra=user, study=study1)
        baker.make('studies.Site', cra=user, study=study1)
        qs = Study.objects.list(user)
        self.assertEqual(1, len(qs))


class StudyItemManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(StudyItemManagerTestCase, self).setUp()

    def test_owner(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')
        study_item1 = baker.make('studies.StudyItem', study=study1)
        study_item2 = baker.make('studies.StudyItem', study=study2)
        qs = StudyItem.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(study_item1.id, qs[0].id)

    def test_company(self):
        c1 = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', company=c1)
        study1 = baker.make('studies.Study', company=c1)
        study2 = baker.make('studies.Study', company=c2)
        study_item1 = baker.make('studies.StudyItem', study=study2)
        study_item2 = baker.make('studies.StudyItem', study=study1)
        qs = StudyItem.objects.company(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(study_item2.id, qs[0].id)


class PatientManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(PatientManagerTestCase, self).setUp()

    def test_owner(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        site1 = baker.make('studies.Site', study=study1)
        site2 = baker.make('studies.Site', study=study2)
        obj1 = baker.make('studies.Patient', study=study1, arm=arm1, site=site1)
        obj2 = baker.make('studies.Patient', study=study2, arm=arm2, site=site2)
        qs = Patient.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_owner_cra(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study', company=c)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        site1 = baker.make('studies.Site', study=study1, cra=user)
        site2 = baker.make('studies.Site', study=study2)
        obj1 = baker.make('studies.Patient', study=study1, arm=arm1, site=site1)
        obj2 = baker.make('studies.Patient', study=study2, arm=arm2, site=site2)
        qs = Patient.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_company(self):
        c1 = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', company=c1)
        study1 = baker.make('studies.Study', company=c1)
        study2 = baker.make('studies.Study', company=c2)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        site1 = baker.make('studies.Site', study=study1)
        site2 = baker.make('studies.Site', study=study2)
        obj1 = baker.make('studies.Patient', study=study2, arm=arm1, site=site1)
        obj2 = baker.make('studies.Patient', study=study1, arm=arm2, site=site2)
        qs = Patient.objects.company(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj2.id, qs[0].id)

    def test_in_progress(self):
        obj1 = baker.make('studies.Patient', status=constants.STUDY_PATIENT_STATUS_TERMINATED)
        obj2 = baker.make('studies.Patient', status=constants.STUDY_PATIENT_STATUS_ACTIVE)
        qs = Patient.objects.in_progress().order_by('id')
        self.assertEqual(1, len(qs))
        self.assertEqual(obj2, qs[0])

    def test_flagged(self):
        obj1 = baker.make('studies.Patient')
        obj2 = baker.make('studies.Patient')
        utils.mark_patient_as_flagged(obj1)
        qs = Patient.objects.flagged()
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1, qs[0])

    def test_not_flagged(self):
        obj1 = baker.make('studies.Patient')
        obj2 = baker.make('studies.Patient')
        utils.mark_patient_as_flagged(obj1)
        qs = Patient.objects.not_flagged()
        self.assertEqual(1, len(qs))
        self.assertEqual(obj2, qs[0])


class VisitManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(VisitManagerTestCase, self).setUp()

    def test_owner(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        obj1 = baker.make('studies.Visit', study=study1, arm=arm1)
        obj2 = baker.make('studies.Visit', study=study2, arm=arm2)
        qs = Visit.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_company(self):
        c1 = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', company=c1)
        study1 = baker.make('studies.Study', company=c1)
        study2 = baker.make('studies.Study', company=c2)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        obj1 = baker.make('studies.Visit', study=study2, arm=arm1)
        obj2 = baker.make('studies.Visit', study=study1, arm=arm2)
        qs = Visit.objects.company(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj2.id, qs[0].id)

    def test_update_order_up(self):
        obj1 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, order=1)
        obj2 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, arm=obj1.arm, order=2)
        obj3 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, arm=obj1.arm, order=3)
        # posouvám jakoby obj1 z 1. pozice na 2., takže by se dvojka měla přesunout na 1
        Visit.objects.update_order(obj1.arm, 1, 2)
        obj1.refresh_from_db()
        obj2.refresh_from_db()
        obj3.refresh_from_db()
        self.assertEqual(1, obj1.order)  # protože přesouvám "jakoby", tak obj1 zůstává na order=1
        self.assertEqual(1, obj2.order)
        self.assertEqual(3, obj3.order)

    def test_update_order_down(self):
        obj1 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, order=1)
        obj2 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, arm=obj1.arm, order=2)
        obj3 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, arm=obj1.arm, order=3)
        # posouvám jakoby obj3 z 3. pozice na 1.
        Visit.objects.update_order(obj1.arm, 3, 1)
        obj1.refresh_from_db()
        obj2.refresh_from_db()
        obj3.refresh_from_db()
        self.assertEqual(2, obj1.order)
        self.assertEqual(3, obj2.order)
        self.assertEqual(3, obj3.order)  # protože přesouvám "jakoby", tak obj3 zůstává na order=3

    def test_update_order_new(self):
        obj1 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, order=1)
        obj2 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, arm=obj1.arm, order=2)
        obj3 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, arm=obj1.arm, order=3)
        # posouvám jakoby obj1 z 1. pozice na 2., takže by se dvojka měla přesunout na 1
        Visit.objects.update_order(obj1.arm, None, 2)
        obj1.refresh_from_db()
        obj2.refresh_from_db()
        obj3.refresh_from_db()
        self.assertEqual(1, obj1.order)
        self.assertEqual(3, obj2.order)
        self.assertEqual(4, obj3.order)

    def test_update_order_delete(self):
        obj1 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, order=1)
        obj2 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, arm=obj1.arm, order=2)
        obj3 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR, arm=obj1.arm, order=3)
        # mažu jakoby obj2 z 2. pozice, takže by se měly všechny vyšší objekty poslat dolů
        Visit.objects.update_order(obj1.arm, 2, None)
        obj1.refresh_from_db()
        obj2.refresh_from_db()
        obj3.refresh_from_db()
        self.assertEqual(1, obj1.order)
        self.assertEqual(2, obj2.order)
        self.assertEqual(2, obj3.order)


class VisitItemManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(VisitItemManagerTestCase, self).setUp()

    def test_owner(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        visit1 = baker.make('studies.Visit', study=study1, arm=arm1)
        visit2 = baker.make('studies.Visit', study=study2, arm=arm2)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        study_item2 = baker.make('studies.StudyItem', study=study2)
        obj1 = baker.make('studies.VisitItem', study=study1, visit=visit1, study_item=study_item1)
        obj2 = baker.make('studies.VisitItem', study=study2, visit=visit2, study_item=study_item2)
        qs = VisitItem.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_company(self):
        c1 = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', company=c1)
        study1 = baker.make('studies.Study', company=c1)
        study2 = baker.make('studies.Study', company=c2)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        visit1 = baker.make('studies.Visit', study=study1, arm=arm1)
        visit2 = baker.make('studies.Visit', study=study2, arm=arm2)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        study_item2 = baker.make('studies.StudyItem', study=study2)
        obj1 = baker.make('studies.VisitItem', study=study1, visit=visit1, study_item=study_item1)
        obj2 = baker.make('studies.VisitItem', study=study2, visit=visit2, study_item=study_item2)
        qs = VisitItem.objects.company(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)


class PatientVisitManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(PatientVisitManagerTestCase, self).setUp()

    def test_owner_admin(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)

        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')

        site1 = baker.make('studies.Site', study=study1)
        site2 = baker.make('studies.Site', study=study2)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        patient1 = baker.make('studies.Patient', site=site1, study=study1, arm=arm1)
        patient2 = baker.make('studies.Patient', site=site2, study=study2, arm=arm2)
        visit1 = baker.make('studies.Visit', study=study1, arm=arm1)
        visit2 = baker.make('studies.Visit', study=study2, arm=arm2)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        study_item2 = baker.make('studies.StudyItem', study=study2)
        visit_item1 = baker.make('studies.VisitItem', study=study1, visit=visit1, study_item=study_item1)
        visit_item2 = baker.make('studies.VisitItem', study=study2, visit=visit2, study_item=study_item2)
        obj1 = baker.make('studies.PatientVisit', study=study1, patient=patient1, visit=visit1)
        obj2 = baker.make('studies.PatientVisit', study=study2, patient=patient2, visit=visit2)
        qs = PatientVisit.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_owner_cra(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)

        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')

        site1 = baker.make('studies.Site', study=study1, cra=user)
        site2 = baker.make('studies.Site', study=study2)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        patient1 = baker.make('studies.Patient', site=site1, study=study1, arm=arm1)
        patient2 = baker.make('studies.Patient', site=site2, study=study2, arm=arm2)
        visit1 = baker.make('studies.Visit', study=study1, arm=arm1)
        visit2 = baker.make('studies.Visit', study=study2, arm=arm2)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        study_item2 = baker.make('studies.StudyItem', study=study2)
        visit_item1 = baker.make('studies.VisitItem', study=study1, visit=visit1, study_item=study_item1)
        visit_item2 = baker.make('studies.VisitItem', study=study2, visit=visit2, study_item=study_item2)
        obj1 = baker.make('studies.PatientVisit', study=study1, patient=patient1, visit=visit1)
        obj2 = baker.make('studies.PatientVisit', study=study2, patient=patient2, visit=visit2)
        qs = PatientVisit.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_company(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)

        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')

        site1 = baker.make('studies.Site', study=study1, cra=user)
        site2 = baker.make('studies.Site', study=study2)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        patient1 = baker.make('studies.Patient', site=site1, study=study1, arm=arm1)
        patient2 = baker.make('studies.Patient', site=site2, study=study2, arm=arm2)
        visit1 = baker.make('studies.Visit', study=study1, arm=arm1)
        visit2 = baker.make('studies.Visit', study=study2, arm=arm2)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        study_item2 = baker.make('studies.StudyItem', study=study2)
        visit_item1 = baker.make('studies.VisitItem', study=study1, visit=visit1, study_item=study_item1)
        visit_item2 = baker.make('studies.VisitItem', study=study2, visit=visit2, study_item=study_item2)
        obj1 = baker.make('studies.PatientVisit', study=study1, patient=patient1, visit=visit1)
        obj2 = baker.make('studies.PatientVisit', study=study2, patient=patient2, visit=visit2)
        qs = PatientVisit.objects.company(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_discontinual(self):
        self.visit1 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL)
        self.visit2 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        self.obj1 = baker.make('studies.PatientVisit', visit=self.visit1)
        self.obj2 = baker.make('studies.PatientVisit', visit=self.visit2)
        qs = PatientVisit.objects.discontinual()
        self.assertEqual(1, len(qs))
        self.assertEqual(self.obj1, qs[0])

    def test_regular(self):
        self.visit1 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL)
        self.visit2 = baker.make('studies.Visit', visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        self.obj1 = baker.make('studies.PatientVisit', visit=self.visit1)
        self.obj2 = baker.make('studies.PatientVisit', visit=self.visit2)
        qs = PatientVisit.objects.regular()
        self.assertEqual(1, len(qs))
        self.assertEqual(self.obj2, qs[0])


class PatientVisitItemManagerTestCase(TestCase):

    def setUp(self) -> None:
        super(PatientVisitItemManagerTestCase, self).setUp()

    def test_owner_admin(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)

        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')

        site1 = baker.make('studies.Site', study=study1)
        site2 = baker.make('studies.Site', study=study2)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        patient1 = baker.make('studies.Patient', site=site1, study=study1, arm=arm1)
        patient2 = baker.make('studies.Patient', site=site2, study=study2, arm=arm2)
        visit1 = baker.make('studies.Visit', study=study1, arm=arm1)
        visit2 = baker.make('studies.Visit', study=study2, arm=arm2)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        study_item2 = baker.make('studies.StudyItem', study=study2)
        visit_item1 = baker.make('studies.VisitItem', study=study1, visit=visit1, study_item=study_item1)
        visit_item2 = baker.make('studies.VisitItem', study=study2, visit=visit2, study_item=study_item2)
        pv1 = baker.make('studies.PatientVisit', study=study1, patient=patient1, visit=visit1)
        pv2 = baker.make('studies.PatientVisit', study=study2, patient=patient2, visit=visit2)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=pv1, visit_item=visit_item1)
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=pv2, visit_item=visit_item2)
        qs = PatientVisitItem.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_owner_cra(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)

        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')

        site1 = baker.make('studies.Site', study=study1, cra=user)
        site2 = baker.make('studies.Site', study=study2)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        patient1 = baker.make('studies.Patient', site=site1, study=study1, arm=arm1)
        patient2 = baker.make('studies.Patient', site=site2, study=study2, arm=arm2)
        visit1 = baker.make('studies.Visit', study=study1, arm=arm1)
        visit2 = baker.make('studies.Visit', study=study2, arm=arm2)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        study_item2 = baker.make('studies.StudyItem', study=study2)
        visit_item1 = baker.make('studies.VisitItem', study=study1, visit=visit1, study_item=study_item1)
        visit_item2 = baker.make('studies.VisitItem', study=study2, visit=visit2, study_item=study_item2)
        pv1 = baker.make('studies.PatientVisit', study=study1, patient=patient1, visit=visit1)
        pv2 = baker.make('studies.PatientVisit', study=study2, patient=patient2, visit=visit2)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=pv1, visit_item=visit_item1)
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=pv2, visit_item=visit_item2)
        qs = PatientVisitItem.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_company(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)

        study1 = baker.make('studies.Study', company=c)
        study2 = baker.make('studies.Study')

        site1 = baker.make('studies.Site', study=study1, cra=user)
        site2 = baker.make('studies.Site', study=study2)
        arm1 = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study2)
        patient1 = baker.make('studies.Patient', site=site1, study=study1, arm=arm1)
        patient2 = baker.make('studies.Patient', site=site2, study=study2, arm=arm2)
        visit1 = baker.make('studies.Visit', study=study1, arm=arm1)
        visit2 = baker.make('studies.Visit', study=study2, arm=arm2)
        study_item1 = baker.make('studies.StudyItem', study=study1)
        study_item2 = baker.make('studies.StudyItem', study=study2)
        visit_item1 = baker.make('studies.VisitItem', study=study1, visit=visit1, study_item=study_item1)
        visit_item2 = baker.make('studies.VisitItem', study=study2, visit=visit2, study_item=study_item2)
        pv1 = baker.make('studies.PatientVisit', study=study1, patient=patient1, visit=visit1)
        pv2 = baker.make('studies.PatientVisit', study=study2, patient=patient2, visit=visit2)
        obj1 = baker.make('studies.PatientVisitItem', patient_visit=pv1, visit_item=visit_item1)
        obj2 = baker.make('studies.PatientVisitItem', patient_visit=pv2, visit_item=visit_item2)
        qs = PatientVisitItem.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1.id, qs[0].id)

    def test_get_reims_sum(self):
        _ = baker.make('studies.PatientVisitItem', visit_item__study_item__price=100)
        _ = baker.make('studies.PatientVisitItem', visit_item__study_item__price=200)
        self.assertEqual(300, PatientVisitItem.objects.get_reims_sum())

    def test_for_study(self):
        study = baker.make('studies.Study')
        obj1 = baker.make('studies.PatientVisitItem', patient_visit__study=study)
        _ = baker.make('studies.PatientVisitItem')
        qs = PatientVisitItem.objects.for_study(study)
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1, qs[0])

    def test_not_processed(self):
        _ = baker.make('studies.PatientVisitItem', approved=True)
        obj1 = baker.make('studies.PatientVisitItem')
        qs = PatientVisitItem.objects.not_processed()
        self.assertEqual(1, len(qs))
        self.assertEqual(obj1, qs[0])
