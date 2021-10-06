from django.conf import settings
from django.test import TestCase

from model_bakery import baker
from requests import Request

from main.apps.studies.models import Visit
from main.apps.studies import constants as study_constants
from main.apps.users import constants as user_constants

from ... import constants, serializers, utils


class PatientVisitItemSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(PatientVisitItemSerializerTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.study1 = baker.make('studies.Study', company=self.c1, status=study_constants.STUDY_STATUS_PROGRESS)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        utils.create_visits(self.study1, self.arm1)
        self.visit1 = Visit.objects.regular().first()
        self.site1 = baker.make('studies.Site', study=self.study1)
        self.patient1 = baker.make('studies.Patient', arm=self.arm1, site=self.site1, study=self.study1)
        self.study_item1 = baker.make('studies.StudyItem', study=self.study1, price=100)
        self.visit_item = baker.make('studies.VisitItem', study=self.study1, visit=self.visit1, study_item=self.study_item1)
        self.patient_visit = baker.make('studies.PatientVisit', patient=self.patient1, visit=self.visit1, study=self.study1)
        self.request = Request()
        self.request.user = self.user

    def test_keys(self):
        pvi = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item,
                         approved=True)
        self.assertEqual(
            ['id', 'patient_visit', 'visit_item_obj', 'patient_obj', 'date', 'approved', 'status', 'origin', 'reject_reason', 'flagged', 'can_be_deleted'],
            list(serializers.PatientVisitItemSerializer(pvi).data.keys())
        )

    def test_validation_success(self):
        serializer = serializers.PatientVisitItemSerializer(data={
            'visit_item': self.visit_item.id,
            'patient_visit': self.patient_visit.id,
        }, context={'request': self.request})
        self.assertTrue(serializer.is_valid())

    def test_validation_approved(self):
        pvi = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item, approved=True)
        serializer = serializers.PatientVisitItemSerializer(pvi, data={
            'approved': False
        }, context={'request': self.request}, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('approved' in serializer.errors.keys())

    def test_validation_credit_balance_success(self):
        baker.make('credit.CreditBalance', balance_sum=1000 * settings.INT_RATIO, study=self.study1)
        pvi = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item, approved=None)
        serializer = serializers.PatientVisitItemSerializer(pvi, data={
            'approved': True
        }, context={'request': self.request}, partial=True)
        self.assertTrue(serializer.is_valid())

    def test_validation_credit_balance_failed(self):
        baker.make('credit.CreditBalance', balance_sum=100 * settings.INT_RATIO, study=self.study1)
        pvi = baker.make('studies.PatientVisitItem', patient_visit=self.patient_visit, visit_item=self.visit_item, approved=None)
        serializer = serializers.PatientVisitItemSerializer(pvi, data={
            'approved': True
        }, context={'request': self.request}, partial=True)
        self.assertFalse(serializer.is_valid())

    def test_validation_patient_visit_failed(self):
        # vytvořím PatientVisit pro jiného pacienta
        patient_visit = baker.make('studies.PatientVisit', visit=self.visit1, study=self.study1)

        serializer = serializers.PatientVisitItemSerializer(data={
            'visit_item': self.visit_item.id,
            'patient_visit': patient_visit.id,
        },
            context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('patient_visit' in serializer.errors.keys())

    def test_validation_visit_item_failed(self):
        # vytvořím VisitItem pro jinou visitu než je PatientVisit
        visit_item = baker.make('studies.VisitItem', study=self.study1, visit=Visit.objects.discontinual().first(), study_item=self.study_item1)

        serializer = serializers.PatientVisitItemSerializer(data={
            'visit_item': visit_item.id,
            'patient_visit': self.patient_visit.id,
        },
            context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('visit_item' in serializer.errors.keys())

    def test_save(self):
        data = {
            'visit_item': self.visit_item.id,
            'patient_visit': self.patient_visit.id,
        }
        serializer = serializers.PatientVisitItemSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        saved_data = {
            'visit_item': instance.visit_item.id,
            'patient_visit': instance.patient_visit.id,
        }
        self.assertEqual(
            data,
            saved_data,
        )
        self.assertEqual(constants.STUDY_PATIENT_VISIT_ITEM_ORIGIN_CRA, instance.origin)
