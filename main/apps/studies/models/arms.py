from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from simple_history.models import HistoricalRecords

from main.libraries.models import BaseModel
from ..managers import ArmQuerySet
from .. import constants


class Arm(BaseModel):
    objects = ArmQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', verbose_name=_('study'), related_name='arms', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255)
    max_unscheduled = models.PositiveSmallIntegerField(_('value'), default=0)
    deleted = models.BooleanField(default=False)

    d_visit_items_cost = models.PositiveIntegerField(default=0)

    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at', 'd_visit_items_cost'])

    class Meta:
        verbose_name = _('arm')
        verbose_name_plural = _('arms')

    def __str__(self):
        return self.title

    def is_owner(self, user):
        if user.is_anonymous:
            return False
        return self.study.is_owner(user)

    @cached_property
    def discontinual_visit(self):
        return self.visits.filter(visit_type=constants.STUDY_VISIT_TYPE_DISCONTINUAL).first()

    def get_group_obj_id(self):
        return self.study_id

    def custom_delete(self):
        """ Pokud je studie ve stavu DRAFt tak smažu celý objekt z DB. Jinak pouze soft delete. """
        if self.study.status in [constants.STUDY_STATUS_DRAFT]:
            self.delete()
        else:
            self.deleted = True
            self.save()

    def set_d_visit_items_cost(self, value):
        self.d_visit_items_cost = value
        self.save()
