from django.test import TestCase

from model_bakery import baker
from requests import Request

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER
from main.apps.users import constants as user_constants

from ... import serializers


class VisitItemSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(VisitItemSerializerTestCase, self).setUp()
        self.c1 = baker.make('companies.Company')
        self.user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=self.c1)
        self.study1 = baker.make('studies.Study', company=self.c1)
        self.arm1 = baker.make('studies.Arm', study=self.study1)
        self.visit1 = baker.make('studies.Visit', study=self.study1, arm=self.arm1)
        self.study_item1 = baker.make('studies.StudyItem', study=self.study1)
        self.request = Request()
        self.request.user = self.user

    def test_validation_success(self):
        serializer = serializers.VisitItemSerializer(data={
            'visit': self.visit1.id,
            'study_item': self.study_item1.id,
        },
            context={'request': self.request})
        self.assertTrue(serializer.is_valid())

    def test_validation_visit_failed(self):
        visit2 = baker.make('studies.Visit')
        serializer = serializers.VisitItemSerializer(data={
            'visit': visit2.id,
            'study_item': self.study_item1.id,
        },
            context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('visit' in serializer.errors.keys())

    def test_validation_study_item_failed(self):
        study_item2 = baker.make('studies.StudyItem')
        serializer = serializers.VisitItemSerializer(data={
            'visit': self.visit1.id,
            'study_item': study_item2.id,
        },
            context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('study_item' in serializer.errors.keys())

    def test_validation_study_failed(self):

        study2 = baker.make('studies.Study', company=self.c1)
        study_item2 = baker.make('studies.StudyItem', study=study2)

        # nematchuje study_item.study a visit.study
        serializer = serializers.VisitItemSerializer(data={
            'visit': self.visit1.id,
            'study_item': study_item2.id,
        },
            context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('visit' in serializer.errors.keys())

    def test_save(self):
        data = {
            'visit': self.visit1.id,
            'study_item': self.study_item1.id,
        }
        serializer = serializers.VisitItemSerializer(data=data, context={'request': self.request})
        if not serializer.is_valid():
            print(serializer.errors)
        instance = serializer.save()
        saved_data = {
            'visit': instance.visit.id,
            'study_item': instance.study_item.id,
        }
        self.assertEqual(
            data,
            saved_data,
        )
