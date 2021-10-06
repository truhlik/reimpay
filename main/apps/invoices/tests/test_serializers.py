from django.test import TestCase
from model_bakery import baker

from ..serializers import InvoiceSerializer


class InvoiceSerializersTestCase(TestCase):

    def setUp(self) -> None:
        super(InvoiceSerializersTestCase, self).setUp()

    def test_keys(self):
        obj = baker.make('invoices.Invoice')
        serializer = InvoiceSerializer(obj)
        self.assertEqual(
            [
                'id',
                'company',
                'fakturoid_public_url',
                'invoice_number',
                'issue_date',
                'amount',
                'status',
            ],
            list(serializer.data),
        )
