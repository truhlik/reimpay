from django.conf import settings
from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.credit.serializers import CreditBalanceSerializer


class CreditBalanceSerializerTestCase(APITestCase):

    def setUp(self) -> None:
        super(CreditBalanceSerializerTestCase, self).setUp()

    def test_keys(self):
        cb1 = baker.make('credit.CreditBalance')
        serializer = CreditBalanceSerializer(cb1)
        self.assertEqual(
            list(serializer.data.keys()),
            ['id', 'balance_type', 'balance_amount', 'created_at']
        )

    def test_balance_amount(self):
        cb1 = baker.make('credit.CreditBalance', balance_amount=1.34 * settings.INT_RATIO)
        serializer = CreditBalanceSerializer(cb1)
        self.assertEqual("1.34 CZK", serializer.data['balance_amount'])

