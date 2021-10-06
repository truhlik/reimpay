from django.test import TestCase

from model_bakery import baker

from ..serializers import BaseCompanySerializer


class CompanySerializersTestCase(TestCase):

    def setUp(self) -> None:
        super(CompanySerializersTestCase, self).setUp()

    def test_company_read_serializer_keys(self):
        c1 = baker.make('companies.Company')
        self.assertSetEqual(set(['id', 'image', 'reg_number',
                                 'name', 'description', 'email', 'phone', 'web', 'vat_number', 'street',
                                 'street_number', 'city', 'zip', 'address']),
                            set(BaseCompanySerializer(c1).data.keys()))

    def test_write_serializer_validate_success(self):
        data = {
            "role": "CONSULTANT",
            "name": "Luboš Truhlář",
            "description": "",
            "email": "lubos.truhlar@gmail.com",
            "phone": "777000112",
            "web": "www.endevel.cz",
            "reg_number": "07328958",
            "vat_number": "",
            "street": "U Stadionu",
            "street_number": "1",
            "city": "Kralupy Nad Vltavou",
            "zip": "27801"
        }
        serializer = BaseCompanySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_write_serializer_validate_without_web(self):
        data = {
            "role": "CONSULTANT",
            "name": "Luboš Truhlář",
            "description": "",
            "email": "lubos.truhlar@gmail.com",
            "phone": "777000112",
            "web": "",
            "reg_number": "07328958",
            "vat_number": "",
            "street": "U Stadionu",
            "street_number": "1",
            "city": "Kralupy Nad Vltavou",
            "zip": "27801"
        }
        serializer = BaseCompanySerializer(data=data)
        self.assertTrue(serializer.is_valid())

