from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from simple_history.models import HistoricalRecords

from main.libraries.models import BaseModel
from ..managers import VisitItemQuerySet
from .. import constants


class VisitItem(BaseModel):
    objects = VisitItemQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', verbose_name=_('study'), related_name='visit_items', on_delete=models.CASCADE)
    visit = models.ForeignKey('studies.Visit', verbose_name=_('visit'), related_name='visit_items', on_delete=models.CASCADE)
    study_item = models.ForeignKey('studies.StudyItem', verbose_name=_('study item'), related_name='visit_items', on_delete=models.CASCADE)
    deleted = models.BooleanField(_('deleted'), default=False)

    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at'])

    class Meta:
        verbose_name = _('visit item')
        verbose_name_plural = _('visit items')

    def __str__(self):
        return self.study_item.title

    def clean(self):
        super(VisitItem, self).clean()

        # pokud mám studii, tak musím cleanovat integritu dat
        if self.study_id is not None:
            if self.visit_id is not None and self.visit.study_id != self.study_id:
                raise ValidationError({'visit': _('IntegrityError: this arm does not belong to given study')})
            if self.study_item_id is not None and self.study_item.study_id != self.study_id:
                raise ValidationError(
                    {'study_item': _('IntegrityError: this study_item does not belong to given study')})

    def custom_delete(self):
        """ Pokud je studie ve stavu PRELAUNCH tak smažu celý objekt z DB. Jinak pouze soft delete. """
        if self.study.status in [constants.STUDY_STATUS_DRAFT]:
            self.delete()
        else:
            self.deleted = True
            self.save()

    def get_group_obj_id(self):
        return self.study_id

    def is_owner(self, user):
        if user.is_anonymous:
            return False
        return self.study.is_owner(user)

    def save(self, *args, **kwargs):
        if self.study_id is None:
            self.study_id = self.visit.study_id

        super(VisitItem, self).save(*args, **kwargs)

        # spočítej celkovou cenu všech visit items v Armu a ulož to na něj
        from main.apps.studies.utils.visit_item_utils import get_visit_item_cost
        self.visit.arm.set_d_visit_items_cost(get_visit_item_cost(self.visit.arm))
