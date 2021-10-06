from django.db import models

from main.apps.ticket.managers import TicketQuerySet
from main.libraries.models import BaseModel


class Ticket(BaseModel):
    objects = TicketQuerySet.as_manager()
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=1024)
    text = models.TextField()
    sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'ticket'
        verbose_name_plural = 'tickets'

    def __str__(self):
        return self.subject
