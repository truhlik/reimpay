from django.db import models


class TicketQuerySet(models.QuerySet):

    def not_sent(self):
        return self.filter(sent_at__isnull=True)
