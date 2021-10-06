from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users.constants import USER_ROLE_ADMIN


class TicketViewTestCase(APITestCase):

    def setUp(self) -> None:
        super(TicketViewTestCase, self).setUp()
        self.user = baker.make('users.User', role=USER_ROLE_ADMIN)

    def do_auth(self):
        self.client.force_authenticate(user=self.user)

    def test_post_unauth(self):
        data = {
            'email': 'lubos.truhlar@gmail.com',
            'subject': 'test',
            'text': 'test',
        }
        r = self.client.post(reverse('ticket-list'), data=data)
        self.assertEqual(401, r.status_code)

    def test_post_auth(self):
        self.do_auth()
        data = {
            'email': 'lubos.truhlar@gmail.com',
            'subject': 'test',
            'text': 'test',
        }
        r = self.client.post(reverse('ticket-list'), data=data)
        self.assertEqual(201, r.status_code)
