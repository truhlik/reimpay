from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from simple_history.models import HistoricalRecords

from main.libraries.models import BaseModel
from ..managers import VisitQuerySet
from .. import constants


class Visit(BaseModel):
    objects = VisitQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', verbose_name=_('study'), related_name='visits', on_delete=models.CASCADE)
    arm = models.ForeignKey('studies.Arm', verbose_name=_('arm'), related_name='visits', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255, blank=True, null=True)
    number = models.PositiveSmallIntegerField(_('max unscheduled'), default=0)
    order = models.PositiveSmallIntegerField(_('order'), blank=True, null=True)
    visit_type = models.CharField(_('visit type'), choices=constants.STUDY_VISIT_TYPE_CHOICES, max_length=32)
    deleted = models.BooleanField(_('deleted'), default=False)

    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at'])

    class Meta:
        verbose_name = _('visit')
        verbose_name_plural = _('visits')

    def __init__(self, *args, **kwargs):
        super(Visit, self).__init__(*args, **kwargs)
        self._old_order = self.order
        self._deleted = self.deleted

    def __str__(self):
        if self.visit_type == constants.STUDY_VISIT_TYPE_DISCONTINUAL:
            return 'Discontinuation (last) visit extra items'
        elif self.visit_type == constants.STUDY_VISIT_TYPE_UNSCHEDULED:
            return 'Unscheduled visit'
        else:
            return "{}. visit".format(self.order)

    def clean(self):
        super(Visit, self).clean()
        if self.arm.study_id != self.study_id:
            raise ValidationError({'arm': _('IntegrityError: this arm does not belong to given study')})

    def _get_order(self):
        order = 1
        if self.visit_type == constants.STUDY_VISIT_TYPE_REGULAR:
            max_order = Visit.objects.active().regular().filter(arm=self.arm)\
                            .aggregate(max_order=models.Max('order'))['max_order']
            order = max_order + 1 if max_order is not None else 1
        elif self.visit_type == constants.STUDY_VISIT_TYPE_DISCONTINUAL:
            order = constants.STUDY_VISIT_DISCONTINUAL_ORDER
        elif self.visit_type == constants.STUDY_VISIT_TYPE_UNSCHEDULED:
            order = constants.STUDY_VISIT_UNSCHEDULED_ORDER
        return order

    def get_group_obj_id(self):
        return self.study_id

    def is_owner(self, user):
        if user.is_anonymous:
            return False
        return self.study.is_owner(user)

    def custom_delete(self):
        """ Pokud je studie ve stavu PRELAUNCH tak smažu celý objekt z DB. Jinak pouze soft delete. """
        if self.study.status in [constants.STUDY_STATUS_DRAFT]:
            self.delete()
        else:
            self.deleted = True
            self.visit_items.all().update(deleted=True)
            self.save()

    def order_was_changed(self):
        return self._old_order != self.order

    def deleted_was_changed(self):
        return self._deleted != self.deleted

    def make_after_deleted(self):
        # or self.order je tam kvůli tomu, že když vytovřím objekt bez .order
        # a rovnou ten samý objekt bez volání __init__ smažu, tak mám v _old_order None
        Visit.objects.update_order(self.arm, self._old_order or self.order, None)

    def make_after_restored(self):
        Visit.objects.update_order(self.arm, None, self.order)

    def save(self, *args, **kwargs):
        if self.study_id is None:
            self.study_id = self.arm.study_id

        if self.order is None:
            self.order = self._get_order()

        if self.visit_type == constants.STUDY_VISIT_TYPE_UNSCHEDULED:
            self.arm.max_unscheduled = self.number
            self.arm.save()

        # pokud si mi změní stav deleted, tak mi stačí aktualizovat pouze na základě něho
        if self.deleted_was_changed():
            if self.deleted:
                self.make_after_deleted()
            else:
                self.make_after_restored()
        elif self.order_was_changed():
            Visit.objects.update_order(self.arm, self._old_order, self.order)
        elif self._state.adding:
            # vytvářím nový objekt, to je jako bych ho vracel
            Visit.objects.update_order(self.arm, None, self.order)
        super(Visit, self).save(*args, **kwargs)

        # spočítej celkovou cenu všech visit items v Armu a ulož to na něj
        from main.apps.studies.utils.visit_item_utils import get_visit_item_cost
        self.arm.set_d_visit_items_cost(get_visit_item_cost(self.arm))

    def delete(self, using=None, keep_parents=False):
        self.make_after_deleted()
        return super(Visit, self).delete(using, keep_parents)
