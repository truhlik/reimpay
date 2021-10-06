from django.db import models


class TopUpQuerySet(models.QuerySet):

    def owner(self, user):
        if user.is_anonymous:
            return self.none()
        return self.filter(study__company=user.company)
