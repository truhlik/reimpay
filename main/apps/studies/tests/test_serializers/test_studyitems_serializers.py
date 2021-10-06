from django.test import TestCase

from model_bakery import baker
from requests import Request

from main.apps.users import constants as user_constants

from ... import serializers


class StudyItemSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(StudyItemSerializerTestCase, self).setUp()

    def test_validation_study_success(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        study_item1 = baker.make('studies.StudyItem', study=study1)

        request = Request()
        request.user = user

        study2 = baker.make('studies.Study', company=c)
        serializer = serializers.StudyItemSerializer(data={
            'title': 'test',
            'description': 'test',
            'price': 100,
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

        study1 = baker.make('studies.Study', company=c)
        study_item1 = baker.make('studies.StudyItem', study=study1)

        study2 = baker.make('studies.Study', company=c2)
        serializer = serializers.StudyItemSerializer(data={
            'title': 'test',
            'description': 'test',
            'price': 100,
            'study': str(study2.id),
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())

    def test_save(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)
        study_item1 = baker.make('studies.StudyItem', study=study1)

        request = Request()
        request.user = user

        study2 = baker.make('studies.Study', company=c2)
        data = {
            'title': 'test',
            'description': 'test',
            'price': 100,
            'study': study1.id,
        }
        serializer = serializers.StudyItemSerializer(data=data,
                                                     context={'request': request})
        serializer.is_valid()
        instance = serializer.save()
        saved_data = {
            'title': instance.title,
            'description': instance.description,
            'price': instance.price,
            'study': instance.study_id,
        }
        self.assertEqual(
            data,
            saved_data,
        )
