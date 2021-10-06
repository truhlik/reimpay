from django.test import TestCase

from model_bakery import baker
from .. import utils


class CompanyUtilsTestCase(TestCase):

    def setUp(self) -> None:
        super(CompanyUtilsTestCase, self).setUp()

    def test_get_company_data_for_fakturoid(self):
        company = baker.make(
            'companies.Company',
            name="Luboš Truhlář",
            street="U Stadionu",
            street_number="911",
            city="Kralupy nad Vltavou",
            zip="27801",
            reg_number="07328958",
            vat_number="CZ07328958",
            email='info@endevel.cz',
            phone="777000112"
        )
        data = utils.get_company_data_for_fakturoid(company)
        exp_data = {
            'name': "Luboš Truhlář",
            'street': "U Stadionu 911",
            'city': "Kralupy nad Vltavou",
            'zip': "27801",
            'registration_no': "07328958",
            'vat_no': "CZ07328958",
            'email': 'info@endevel.cz',
            'phone': "777000112",
        }
        self.assertEqual(exp_data, data)
