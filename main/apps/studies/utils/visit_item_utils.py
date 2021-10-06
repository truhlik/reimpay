from django.db import models

from ..models import VisitItem


def get_visit_item_cost(arm):
    return VisitItem.objects.active()\
                .regular()\
                .filter(visit__arm=arm)\
                .aggregate(sum=models.Sum('study_item__price'))['sum'] or 0
