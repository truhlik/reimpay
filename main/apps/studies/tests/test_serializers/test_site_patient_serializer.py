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
        serializer = serializers.SitePatientSerializer(site)
        self.assertEqual(
            [
                'patients',
                'id',
                'title',
                'study',
                'expected_patients',
                'cra',
                'contract_path',
                'site_instructions_path',
            ],
            list(serializer.data.keys())
        )

    def test_values(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c2, first_name='lubos')
        request = Request()
        request.user = cra

        study2 = baker.make('studies.Study', company=c)
        site = baker.make('studies.Site', study=study2, cra=cra)
        serializer = serializers.SitePatientSerializer(instance=site)

        self.assertEqual('http://example.com/api/v1/sites/{}/patient/pdf/'.format(site.id, site.pin),
                         serializer.data['contract_path'])
        self.assertEqual('http://example.com/api/v1/sites/{}/instruction/pdf/'.format(site.id, site.pin),
                         serializer.data['site_instructions_path'])
        self.assertEqual([],
                         serializer.data['patients'])
