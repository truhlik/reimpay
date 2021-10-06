from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField  # noqa

from main.libraries.models import BaseModel
from main.libraries.utils import get_location_format
from .managers import CompanyQuerySet
from .utils import company_dir_path


class Company(BaseModel):
    objects = CompanyQuerySet.as_manager()

    name = models.CharField(_('obchodní název'), max_length=512, db_index=True)
    # image = ImageField(_('obrázek'), upload_to=company_dir_path, blank=True, null=True)
    image = models.ImageField(_('obrázek'), upload_to=company_dir_path, blank=True, null=True)
    description = models.TextField(_('popis'), blank=True, null=True)
    data = JSONField(_('data'), default=dict, blank=True, null=True)

    email = models.EmailField(_('email'), blank=True, null=True)
    phone = models.CharField(_('telefon'), max_length=32, blank=True, null=True)
    web = models.CharField(_('web'), blank=True, null=True, max_length=255)

    reg_number = models.CharField(_('IČ'), max_length=32, blank=True, null=True)
    vat_number = models.CharField(_('DIČ'), max_length=32, blank=True, null=True)

    commission = models.PositiveSmallIntegerField(default=10)

    street = models.CharField(_('ulice'), max_length=255, blank=True, null=True)
    street_number = models.CharField(_('čp'), max_length=255, blank=True, null=True)
    city = models.CharField(_('město'), max_length=255, blank=True, null=True)
    zip = models.CharField(_('PSČ'), max_length=255, blank=True, null=True)

    fa_subject_id = models.IntegerField('subject_id', blank=True, null=True)

    class Meta:
        verbose_name = 'obchodní subjekt'
        verbose_name_plural = 'obchodní subjekty'

    def __str__(self):
        return self.name

    @property
    def address(self):
        return get_location_format(self.street_number, self.street, self.zip, self.city)

    def is_owner(self, user):
        if user.is_anonymous:
            return False
        elif not user.has_admin_role():
            return False
        return self.users.filter(id=user.id)

    def can_be_deleted(self):
        return False

    def can_be_edit(self):
        return True
