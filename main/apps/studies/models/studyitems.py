from django.db import models
from django.utils.translation import ugettext_lazy as _

from simple_history.models import HistoricalRecords

from main.libraries.models import BaseModel
from ..managers import StudyItemQuerySet
from .. import constants


class StudyItem(BaseModel):
    objects = StudyItemQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', verbose_name=_('study'), related_name='study_items', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255)
    description = models.CharField(_('local language title'), max_length=2048)
    price = models.PositiveSmallIntegerField(_('value'))
    deleted = models.BooleanField(_('deleted'), default=False)

    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at'])

    class Meta:
        verbose_name = _('study item')
        verbose_name_plural = _('study items')

    def __str__(self):
        return self.title

    def get_group_obj_id(self):
        return self.study_id

    def is_owner(self, user):
        if user.is_anonymous:
            return False
        return self.study.is_owner(user)

    def custom_delete(self):
        """ Pokud je studie ve stavu DRAFt tak smažu celý objekt z DB. Jinak pouze soft delete. """
        if self.study.status in [constants.STUDY_STATUS_DRAFT]:
            self.delete()
        else:
            self.deleted = True
            self.visit_items.all().update(deleted=True)
            self.save()
