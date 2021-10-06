import uuid
from random import random

from django.db import models
from django.utils.translation import ugettext_lazy as _

from simple_history.models import HistoricalRecords

from main.libraries.models import BaseModel
from ..managers import SiteQuerySet
from .. import constants


def get_contract_path(instance, filename):
    return 'site_{0}/{1}/{2}'.format(instance.id, uuid.uuid4(), filename)


class Site(BaseModel):
    objects = SiteQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', verbose_name=_('study'), related_name='sites', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255)
    expected_patients = models.PositiveSmallIntegerField(_('Exp. patients'), default=0)
    cra = models.ForeignKey('users.User', verbose_name=_('cra'), related_name='sites', on_delete=models.SET_NULL, null=True)  # noqa
    pin = models.CharField(_('pin'), max_length=16)
    deleted = models.BooleanField(default=False)

    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at'])

    class Meta:
        verbose_name = _('site')
        verbose_name_plural = _('sites')

    def __str__(self):
        return self.title

    def is_owner(self, user):
        if user.is_anonymous:
            return False
        if user.has_cra_role():
            return self.cra == user
        return self.study.is_owner(user)

    def get_group_obj_id(self):
        return self.study_id

    def custom_delete(self):
        """ Pokud je studie ve stavu PRELAUNCH tak smažu celý objekt z DB. Jinak pouze soft delete. """
        if self.study.status in [constants.STUDY_STATUS_DRAFT]:
            self.delete()
        else:
            self.deleted = True
            self.patients.all().update(deleted=True)
            self.save()

    def save(self, *args, **kwargs):
        if self.pin is None:
            self.pin = random.randrange(100000, 999999)

        super(Site, self).save(*args, **kwargs)
