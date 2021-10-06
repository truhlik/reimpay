from django.test import TestCase
from model_bakery import baker


class PaymentModelTestCase(TestCase):

    def setUp(self) -> None:
        super(PaymentModelTestCase, self).setUp()

    def test_get_vat_value_from_item_value(self):
        payment = baker.prepare('payments.Payment', item_value=100, total_value=None, vat_rate=21)
        self.assertEqual(21, payment._get_vat_value())

    def test_get_vat_value_from_total_value(self):
        payment = baker.prepare('payments.Payment', item_value=None, total_value=121, vat_rate=21)
        self.assertEqual(21, payment._get_vat_value())

    def test_save_without_total_value(self):
        study = baker.make('studies.Study')
        payment = baker.prepare('payments.Payment', item_value=100, total_value=None, vat_rate=21, study=study)
        payment.save()
        self.assertEqual(121, payment.total_value)

    def test_save_without_vat_value(self):
        study = baker.make('studies.Study')
        payment = baker.prepare('payments.Payment', item_value=100, total_value=None, vat_rate=21, study=study)
        payment.save()
        self.assertEqual(21, payment.vat_value)

    def test_save_without_item_value(self):
        study = baker.make('studies.Study')
        payment = baker.prepare('payments.Payment', total_value=121, item_value=None, vat_rate=21, study=study)
        payment.save()
        self.assertEqual(100, payment.item_value)
