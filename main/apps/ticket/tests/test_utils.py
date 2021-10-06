from django.test import TestCase
from django.core import mail

from model_bakery import baker

from ..utils import send_ticket
from ...users.constants import USER_ROLE_ADMIN


class TicketUtilsTestCase(TestCase):

    def setUp(self) -> None:
        super(TicketUtilsTestCase, self).setUp()
        self.user = baker.make('users.User', role=USER_ROLE_ADMIN)

    def test_send_ticket(self):
        ticket = baker.make('ticket.Ticket')
        send_ticket(ticket)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual(ticket.email, mail.outbox[0].reply_to[0])
        self.assertIsNotNone(ticket.sent_at)
