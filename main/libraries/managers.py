from django.db import models


class CustomObjectQueryset(models.QuerySet):

    def active(self):
        return self.filter(trash=False)

    def owner(self, user, trash=False):
        if isinstance(trash, list):
            return self.filter(owner=user, trash__in=trash)
        else:
            return self.filter(owner=user, trash=trash)
