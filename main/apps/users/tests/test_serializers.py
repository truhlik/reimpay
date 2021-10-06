from django.test import TestCase

from model_bakery import baker

from ..serializers import UserSerializer
from .. import constants


class UserSerializersTestCase(TestCase):

    def setUp(self) -> None:
        super(UserSerializersTestCase, self).setUp()

    def test_user_serializer_keys(self):
        c1 = baker.make('users.User')
        self.assertSetEqual(set(['id', 'role', 'first_name', 'last_name', 'email']),
                            set(UserSerializer(c1).data.keys()))

    def test_validation(self):
        data = {
            'first_name': 'test1',
            'last_name': 'test2',
            'email': 'lubos@test.cz',
            'role': constants.USER_ROLE_ADMIN,
        }
        self.assertTrue(UserSerializer(data=data).is_valid())

    def test_validation_fail_role(self):
        data = {
            'first_name': 'test1',
            'last_name': 'test2',
            'email': 'lubos@test.cz',
        }
        self.assertFalse(UserSerializer(data=data).is_valid())

    def test_validation_email(self):
        c1 = baker.make('users.User', email='test@test.cz')
        data = {
            'first_name': 'test1',
            'last_name': 'test2',
            'email': 'test@test.cz',  # nastavim stejny email
            'role': constants.USER_ROLE_ADMIN,
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid(raise_exception=False))
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('email' in serializer.errors.keys())
