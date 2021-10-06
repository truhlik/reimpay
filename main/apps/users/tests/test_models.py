from django.test import TestCase

from model_bakery import baker


class UserSerializersTestCase(TestCase):

    def setUp(self) -> None:
        super(UserSerializersTestCase, self).setUp()

    def test_user_full_name(self):
        u = baker.make('users.User', first_name='Luboš', last_name='Truhlář')
        self.assertEqual('Luboš Truhlář', u.full_name)

    def test_custom_delete(self):
        u = baker.make('users.User', first_name='Luboš', last_name='Truhlář')
        u.custom_delete()
        self.assertFalse(u.is_active)
