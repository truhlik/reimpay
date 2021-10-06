from django.http import HttpRequest
from django.test import TestCase

from model_bakery import baker
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from main.apps.users import constants as user_constants

from ..models import TopUp
from ..serializers import TopUpSerializer


class TopUpSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(TopUpSerializerTestCase, self).setUp()

    def test_keys(self):
        t1 = baker.make(TopUp)
        factory = APIRequestFactory()
        serializer = TopUpSerializer(t1, context={'request': factory.get('/')})
        self.assertEqual(
            ['created_at', 'study', 'amount', 'file'],
            list(serializer.data.keys())
        )

    def test_values(self):
        t1 = baker.make(TopUp, amount=100)
        factory = APIRequestFactory()
        serializer = TopUpSerializer(t1, context={'request': factory.get('/')})
        self.assertEqual(100, serializer.data['amount'])
        self.assertEqual('http://testserver/api/v1/topups/{}/pdf/'.format(t1.id), serializer.data['file'])

    def test_validate(self):
        study1 = baker.make('studies.Study')

        data = {
            'study': study1.id,
            'amount': 10000,
        }
        serializer = TopUpSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_validate_amount_failed(self):
        study1 = baker.make('studies.Study')

        data = {
            'study': study1.id,
            'amount': -100,
        }
        serializer = TopUpSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)

    def test_validate_amount_failed1(self):
        study1 = baker.make('studies.Study')

        data = {
            'study': study1.id,
            'amount': 100,
        }
        serializer = TopUpSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)

    def test_validate_amount_failed2(self):
        study1 = baker.make('studies.Study')

        data = {
            'study': study1.id,
            'amount': 10000,
        }
        serializer = TopUpSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_validate_study_failed(self):
        study1 = baker.make('studies.Study')

        data = {
            'study': '12122',
            'amount': -100,
        }
        serializer = TopUpSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('study', serializer.errors)

    def test_save(self):
        study1 = baker.make('studies.Study')

        data = {
            'study': study1.id,
            'amount': 10000,
        }
        serializer = TopUpSerializer(data=data)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(1, len(TopUp.objects.all()))
