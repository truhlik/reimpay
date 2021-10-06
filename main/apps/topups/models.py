from django.db import models

from main.apps.topups.manager import TopUpQuerySet
from main.libraries.models import BaseModel


class TopUp(BaseModel):
    objects = TopUpQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', related_name='topups', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    file = models.FileField(blank=True, null=True)

    class Meta:
        verbose_name = 'topup'
        verbose_name_plural = 'topups'
