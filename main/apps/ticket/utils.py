from django.conf import settings
from django.utils import timezone

from .models import Ticket
from ...libraries.emails import EmailTicket


def send_tickets():
    for ticket in Ticket.objects.not_sent():
        send_ticket(ticket)


def send_ticket(ticket: Ticket):
    EmailTicket(ticket).send_html_email(settings.DEFAULT_NOTIFICATION_EMAIL, reply_to=[ticket.email])
    ticket.sent_at = timezone.now()
    ticket.save()
