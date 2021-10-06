from django.test import TestCase
from fakturoid import Subject
from constance import config

from .. import utils


class FakturoidTestCase(TestCase):

    def setUp(self) -> None:
        super(FakturoidTestCase, self).setUp()

    def test_create_fakturoid_subject(self):
        data = {
            'name': "Luboš",
            'street': "Truhlář",
            'city': "Kralupy nad Vltavou",
            'zip': "27801",
            'registration_no': "07328958",
            'vat_no': "CZ07328958",
            'email': 'info@endevel.cz',
            'phone': "777000112",
        }
        exp_subject = Subject(
            name="Luboš",
            street="Truhlář",
            city="Kralupy nad Vltavou",
            zip="27801",
            registration_no="07328958",
            vat_no="CZ07328958",
            email='info@endevel.cz',
            phone="777000112",
        )
        config.FAKTUROID_SLUG = 'test'
        config.FAKTUROID_EMAIL = 'test'
        config.FAKTUROID_API_KEY = 'test'
        subject = utils.create_fakturoid_subject(None, data)
        self.assertIsInstance(subject, Subject)
        self.assertEqual(str(exp_subject), str(subject))
