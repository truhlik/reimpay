from django.test import TestCase
from mock import patch

from model_bakery import baker
from requests import Request

from main.apps.users import constants as user_constants

from ... import serializers


class SiteSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(SiteSerializerTestCase, self).setUp()

    def test_keys(self):
        site = baker.make('studies.Site')
        serializer = serializers.SiteSerializer(site)
        self.assertEqual(
            [
                'id',
                'title',
                'study',
                'expected_patients',
                'cra_obj',
                'contract_path',
                'site_instructions_path',
            ],
            list(serializer.data.keys())
        )

    def test_validation_study_success(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)

        request = Request()
        request.user = user

        serializer = serializers.SiteSerializer(data={
            'title': 'test',
            'expected_patients': 100,
            'study': str(study1.id),
            'cra': str(cra.id),
        },
            context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_validation_study_failed(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        request = Request()
        request.user = user

        study2 = baker.make('studies.Study', company=c2)
        serializer = serializers.SiteSerializer(data={
            'title': 'test',
            'expected_patients': 100,
            'study': str(study2.id),
            'cra': str(cra.id),
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('study' in serializer.errors.keys())

    def test_save(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)

        request = Request()
        request.user = user

        data = {
            'title': 'test',
            'expected_patients': 100,
            'study': study1.id,
            'cra': cra.id,
        }
        serializer = serializers.SiteSerializer(data=data,
                                                context={'request': request})
        serializer.is_valid()
        instance = serializer.save()
        saved_data = {
            'title': instance.title,
            'expected_patients': instance.expected_patients,
            'study': instance.study_id,
            'cra': instance.cra_id,
        }
        self.assertEqual(
            data,
            saved_data,
        )
        self.assertIsNot('', instance.pin)

    def test_validation_cra_inactive(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c, is_active=False)
        request = Request()
        request.user = user

        study2 = baker.make('studies.Study', company=c)
        serializer = serializers.SiteSerializer(data={
            'title': 'test',
            'expected_patients': 100,
            'study': str(study2.id),
            'cra': str(cra.id),
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('cra' in serializer.errors.keys())

    def test_validation_cra_admin_role_failed(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        request = Request()
        request.user = user

        study2 = baker.make('studies.Study', company=c)
        serializer = serializers.SiteSerializer(data={
            'title': 'test',
            'expected_patients': 100,
            'study': str(study2.id),
            'cra': str(cra.id),
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('cra' in serializer.errors.keys())

    def test_validation_cra_other_company(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c2)
        request = Request()
        request.user = user

        study2 = baker.make('studies.Study', company=c)
        serializer = serializers.SiteSerializer(data={
            'title': 'test',
            'expected_patients': 100,
            'study': str(study2.id),
            'cra': str(cra.id),
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('cra' in serializer.errors.keys())

    def test_fields_cra_read_serializer(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c2, first_name='lubos')
        request = Request()
        request.user = cra

        study2 = baker.make('studies.Study', company=c)
        site = baker.make('studies.Site', study=study2, cra=cra)
        serializer = serializers.SiteSerializer(instance=site)

        self.assertEqual('lubos', serializer.data['cra_obj']['first_name'])
        self.assertEqual('http://example.com/api/v1/sites/{}/patient/pdf/'.format(site.id, site.pin),
                         serializer.data['contract_path'])
        self.assertEqual('http://example.com/api/v1/sites/{}/instruction/pdf/'.format(site.id, site.pin),
                         serializer.data['site_instructions_path'])

    def test_cra_not_assigned_to_study(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)

        request = Request()
        request.user = user

        serializer = serializers.SiteSerializer(data={
            'title': 'test',
            'expected_patients': 100,
            'study': str(study1.id),
            'cra': str(cra.id),
        },
            context={'request': request})
        self.assertTrue(serializer.is_valid())
