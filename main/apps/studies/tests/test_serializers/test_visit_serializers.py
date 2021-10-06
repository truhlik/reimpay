from django.test import TestCase

from model_bakery import baker
from requests import Request

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER
from main.apps.users import constants as user_constants

from ... import serializers


class VisitSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(VisitSerializerTestCase, self).setUp()

    def test_keys(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        
        study2 = baker.make('studies.Study')  # study from other company
        arm = baker.make('studies.Arm', study=study2)
        visit = baker.make('studies.Visit', arm=arm)
        self.assertEqual(
            ['id', 'arm', 'name', 'title', 'number', 'visit_type', 'visit_items', 'order', 'visit_items_cost'],
            list(serializers.VisitSerializer(visit).data.keys())
        )

    def test_validation_study_success(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        
        arm = baker.make('studies.Arm', study=study1)

        request = Request()
        request.user = user

        serializer = serializers.VisitSerializer(data={
            'arm': arm.id,
            'title': 'test',
        },
            context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_save(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        

        request = Request()
        request.user = user
        arm = baker.make('studies.Arm', study=study1)

        data = {
            'arm': arm.id,
            'title': 'test',
        }
        serializer = serializers.VisitSerializer(data=data,
                                                       context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
        instance = serializer.save()
        saved_data = {
            'arm': instance.arm_id,
            'title': instance.title,
        }
        self.assertEqual(
            data,
            saved_data,
        )

    def test_create_title_generated(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        request = Request()
        request.user = user
        arm = baker.make('studies.Arm', study=study1)

        data = {
            'arm': arm.id,
            'order': 1,
        }
        serializer = serializers.VisitSerializer(data=data,
                                                 context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
        instance = serializer.save()
        self.assertEqual("1. visit", instance.title)

    def test_create_title_defined(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        request = Request()
        request.user = user
        arm = baker.make('studies.Arm', study=study1)

        data = {
            'arm': arm.id,
            'order': 1,
            'title': 'test',
        }
        serializer = serializers.VisitSerializer(data=data,
                                                 context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
        instance = serializer.save()
        self.assertEqual("test", instance.title)

    def test_validate_arm_failed(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        
        study2 = baker.make('studies.Study')  # study from other company
        arm = baker.make('studies.Arm', study=study2)

        request = Request()
        request.user = user

        serializer = serializers.VisitSerializer(data={
            'arm': arm.id,
            'title': 'test',
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('arm' in serializer.errors.keys())

    def test_validate_order_failed(self):
        visit = baker.make('studies.Visit', order=1)

        request = Request()

        serializer = serializers.BaseVisitSerializer(visit, data={
            'order': 0,
        }, partial=True, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('order' in serializer.errors.keys())

    def test_save_with_items(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        study_item = baker.make('studies.StudyItem', study=study1)
        

        request = Request()
        request.user = user
        arm = baker.make('studies.Arm', study=study1)

        data = {
            'arm': arm.id,
            'visit_items': [
                {
                    'study_item': study_item.id
                },
            ]
        }
        serializer = serializers.VisitSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        saved_data = {
            'arm': instance.arm_id,
            'visit_items': [{'study_item': item.study_item_id} for item in instance.visit_items.all()]
        }
        self.assertEqual(
            data,
            saved_data,
        )
