from django.test import TestCase

from model_bakery import baker
from requests import Request

from main.apps.users import constants as user_constants

from ... import serializers


class ArmSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(ArmSerializerTestCase, self).setUp()

    def test_validation_study_success(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        request = Request()
        request.user = user

        serializer = serializers.ArmSerializer(data={
            'title': 'test',
            'max_unscheduled': 100,
            'study': str(study1.id),
        },
            context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_validation_study_failed(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        request = Request()
        request.user = user

        study2 = baker.make('studies.Study', company=c2)
        serializer = serializers.ArmSerializer(data={
            'title': 'test',
            'max_unscheduled': 100,
            'study': str(study2.id),
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())

    def test_save(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        request = Request()
        request.user = user

        data = {
            'title': 'test',
            'max_unscheduled': 0,
            'study': study1.id,
        }
        serializer = serializers.ArmSerializer(data=data,
                                               context={'request': request})
        serializer.is_valid()
        instance = serializer.save()
        saved_data = {
            'title': instance.title,
            'max_unscheduled': instance.max_unscheduled,
            'study': instance.study_id,
        }
        self.assertEqual(
            data,
            saved_data,
        )
