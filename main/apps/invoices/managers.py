from django.db import models


class InvoiceQuerySet(models.QuerySet):

    def owner(self, user):
        if user.is_anonymous:
            return self.none()
        if user.has_admin_role():
            return self.filter(company=user.company)
        else:
            return self.none()
