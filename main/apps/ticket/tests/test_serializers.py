from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory

from model_bakery import baker

from ..models import Ticket
from ..serializers import TicketSerializer
from ...users.constants import USER_ROLE_ADMIN


class TicketSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(TicketSerializerTestCase, self).setUp()
        self.user = baker.make('users.User', role=USER_ROLE_ADMIN)

    def test_user_serializer_keys(self):
        obj = baker.make('ticket.Ticket')
        self.assertEqual(['subject', 'text'],
                         list(TicketSerializer(obj).data.keys()))

    def test_save(self):
        factory = APIRequestFactory()
        request = factory.get('/')
        force_authenticate(request, user=self.user)
        request.user = self.user

        data = {
            'subject': 'test',
            'text': 'test',
        }
        serializer = TicketSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        qs = Ticket.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(self.user, qs[0].user)
