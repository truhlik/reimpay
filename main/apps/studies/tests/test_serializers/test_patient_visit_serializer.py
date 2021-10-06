from django.test import TestCase
from django.utils import timezone

from model_bakery import baker
from requests import Request
from rest_framework.test import APIRequestFactory

from main.apps.studies.models import Visit
from main.apps.users import constants as user_constants
from main.apps.studies import constants as study_constants

from ... import constants, serializers, utils


class PatientVisitSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(PatientVisitSerializerTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.study1 = baker.make('studies.Study', company=self.c1, status=study_constants.STUDY_STATUS_PROGRESS)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        utils.create_visits(self.study1, self.arm1)
        self.site1 = baker.make('studies.Site', study=self.study1)
        self.patient1 = baker.make('studies.Patient', arm=self.arm1, site=self.site1, study=self.study1)
        self.study_item1 = baker.make('studies.StudyItem', study=self.study1)
        factory = APIRequestFactory()
        self.request = factory.get('/')
        self.request.session = {}
        self.request.user = self.user

    def test_keys(self):
        regular = Visit.objects.regular().first()
        pv = baker.make('studies.PatientVisit', patient=self.patient1, visit=regular)

        serializer = serializers.PatientVisitSerializer(pv, context={'request': self.request})
        self.assertEqual(
            ['id', 'patient', 'visit_date', 'visit_items', 'visit', 'title'],
            list(serializer.data.keys())
        )

    def test_validation_success(self):
        serializer = serializers.PatientVisitSerializer(data={
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
        }, context={'request': self.request})
        self.assertTrue(serializer.is_valid())

    def test_save_without_items(self):
        serializer = serializers.PatientVisitSerializer(data={
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
            'visit_items': [],
        }, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        self.assertIsNotNone(serializer.save())

    def test_validation_patient_failed(self):
        patient = baker.make('studies.Patient')
        serializer = serializers.PatientVisitSerializer(data={
            'patient': patient.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
        },
            context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('patient' in serializer.errors.keys())

    def test_validation_visit_date_failed(self):
        serializer = serializers.PatientVisitSerializer(data={
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date()+timezone.timedelta(days=1),
        },
            context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('visit_date' in serializer.errors.keys())

    def test_validation_invalid_patient_already_done_discontinual(self):
        # regular = Visit.objects.regular().first()
        regular2 = baker.make('studies.Visit', arm=self.arm1, visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL)
        baker.make('studies.PatientVisit', patient=self.patient1, visit=regular2)

        serializer = serializers.PatientVisitSerializer(data={
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_DISCONTINUAL,
            'visit_date': timezone.now().date(),
        }, context={'request': self.request})
        self.assertFalse(serializer.is_valid())

    def test_validation_invalid_non_regular_left(self):
        regular = Visit.objects.regular().first()
        baker.make('studies.PatientVisit', patient=self.patient1, visit=regular)

        serializer = serializers.PatientVisitSerializer(data={
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
        }, context={'request': self.request})
        self.assertFalse(serializer.is_valid())

    def test_save(self):
        visit = baker.make('studies.Visit', arm=self.arm1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit_item = baker.make('studies.VisitItem', visit=visit)
        visit_item2 = baker.make('studies.VisitItem', visit=visit)
        visit_item3 = baker.make('studies.VisitItem', visit=visit)

        data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
            'visit_items': [visit_item.id, visit_item2.id, visit_item3.id]
        }
        serializer = serializers.PatientVisitSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        qs = instance.visit_items.all().order_by('id')
        saved_data = {
            'patient': instance.patient_id,
            'visit_type': instance.visit.visit_type,
            'visit_date': instance.visit_date,
            'visit_items': [item.id for item in qs],
        }
        self.assertEqual(
            data,
            saved_data,
        )

    def test_save_origin(self):
        visit = baker.make('studies.Visit', arm=self.arm1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit_item = baker.make('studies.VisitItem', visit=visit)
        visit_item2 = baker.make('studies.VisitItem', visit=visit)
        visit_item3 = baker.make('studies.VisitItem', visit=visit)

        data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
            'visit_items': [visit_item.id, visit_item2.id, visit_item3.id]
        }
        serializer = serializers.PatientVisitSerializer(data=data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        baker.make('studies.PatientVisitItem', origin='CRA', patient_visit=instance)
        pvi_qs = instance.patient_visit_items.all().order_by('-id')
        self.assertEqual(['CRA', 'SITE', 'SITE', 'SITE'], [item.origin for item in pvi_qs])

    def test_validate_visit_items_failed(self):
        visit = baker.make('studies.Visit', arm=self.arm1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)
        visit_item = baker.make('studies.VisitItem', visit=visit)
        visit_item2 = baker.make('studies.VisitItem', visit=visit)
        visit_item3 = baker.make('studies.VisitItem')

        data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_REGULAR,
            'visit_date': timezone.now().date(),
            'visit_items': [visit_item.id, visit_item2.id, visit_item3.id]
        }
        serializer = serializers.PatientVisitSerializer(data=data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertTrue('visit_items' in serializer.errors.keys())

    def test_validate_visit_items_and_patient_failed(self):
        visit = baker.make('studies.Visit', arm=self.arm1, visit_type=constants.STUDY_VISIT_TYPE_REGULAR)

        # označím visitu jako absolvovanou
        baker.make('studies.PatientVisit', patient=self.patient1, visit=visit)

        visit_item = baker.make('studies.VisitItem', visit=visit)
        visit_item2 = baker.make('studies.VisitItem', visit=visit)
        visit_item3 = baker.make('studies.VisitItem', visit=visit)

        data = {
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_DISCONTINUAL,
            'visit_date': timezone.now().date(),
            'visit_items': [visit_item.id, visit_item2.id, visit_item3.id]
        }
        serializer = serializers.PatientVisitSerializer(data=data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertTrue('visit_items' in serializer.errors.keys())

    def test_terminate_patient(self):
        serializer = serializers.PatientVisitSerializer(data={
            'patient': self.patient1.id,
            'visit_type': constants.STUDY_VISIT_TYPE_DISCONTINUAL,
            'visit_date': timezone.now().date(),
        }, context={'request': self.request})
        serializer.is_valid()
        serializer.save()
        self.patient1.refresh_from_db()
        self.assertEqual(constants.STUDY_PATIENT_STATUS_TERMINATED, self.patient1.status)
