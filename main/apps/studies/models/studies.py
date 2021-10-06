from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from simple_history.models import HistoricalRecords

from main.libraries.models import SimpleModel
from main.apps.core import constants as core_constants
from ..managers import StudyQuerySet
from .. import constants


class Study(SimpleModel):
    objects = StudyQuerySet.as_manager()
    status = models.CharField(_('status'), choices=constants.STUDY_STATUS_CHOICES, max_length=64, default=constants.STUDY_STATUS_DRAFT)  # noqa
    number = models.CharField(_('study number'), max_length=255)
    identifier = models.CharField(_('study identifier'), max_length=255)
    notes = models.CharField(_('notes'), blank=True, null=True, max_length=1000)
    operator = models.CharField(_('study operator'), choices=constants.STUDY_OPERATOR_CHOICES, default=constants.STUDY_OPERATOR_SPONSOR, max_length=32)
    sponsor_name = models.CharField(_('Sponsor name'), blank=True, null=True, max_length=255)

    bank_transfer = models.BooleanField(_('bank transfer'), default=False)
    post_office_cash = models.BooleanField(_('czech Post payment order (cash)'), default=False)
    pay_frequency = models.PositiveSmallIntegerField(_('monthly pay frequency'), default=1)
    bank_account = models.CharField(max_length=64, help_text='bankovní účet pro vrácení přeplatku studie', null=True)

    company = models.ForeignKey('companies.Company', related_name='studies', on_delete=models.CASCADE)

    prelaunched_at = models.DateTimeField(blank=True, null=True)
    progress_at = models.DateTimeField(blank=True, null=True)
    billing_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    # admin fields
    commission = models.PositiveSmallIntegerField(default=10)
    variable_symbol = models.BigIntegerField(blank=True, null=True)
    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at', 'prelaunched_at', 'progress_at',
                                                 'billing_at', 'closed_at', 'commission', 'variable_symbol'])

    class Meta:
        verbose_name = _('study')
        verbose_name_plural = _('studies')

    def __init__(self, *args, **kwargs):
        super(Study, self).__init__(*args, **kwargs)
        self._status = self.status

    def __str__(self):
        return self.identifier

    def is_owner(self, user):
        if user.is_anonymous:
            return False
        elif user.has_admin_role():
            return self.company == user.company
        return self.sites.active().filter(cra=user).exists()

    def custom_delete(self):
        """ Pokud je studie ve stavu PRELAUNCH tak smažu celý objekt z DB. Jinak pouze soft delete. """
        if self.status in [constants.STUDY_STATUS_DRAFT]:
            self.delete()
        else:
            self.deleted = True
            self.patients.all().update(deleted=True)
            self.save()

    def date_last_visit(self):
        return timezone.now().date()

    def get_group_obj_id(self):
        return self.id

    def has_been_prelaunched(self):
        """ Vrátí informaci, zda již byla studie Launched. """
        return self.prelaunched_at is not None

    def has_reims(self):
        """ Vrátí informaci, zda má studie nějaké Reims. """
        return bool(self.study_items.active())

    def has_sites(self):
        """ Vrátí informaci, zda má studie nějaké Sites. """
        return bool(self.sites.active())

    def has_been_topup(self):
        """ Vrátí informaci, zda je Studie TOPUPnutá. """
        return self.progress_at is not None  # pokud byla někdy in progres, tak byla topnutá

    def has_visit_map(self):
        """ Vrátí informaci, zda má studie Visit Mapu. """
        return bool(self.arms.active())

    def has_visit_items(self):
        """ Vrátí zda daná studie má nějaké Visit Items."""
        return bool(self.visit_items.active())

    def is_done(self):
        """ Vrátí informaci, zda je studie dokončená. """
        return self.status in [constants.STUDY_STATUS_BILLING, constants.STUDY_STATUS_CLOSED]

    def is_prelaunched(self):
        """ Vrátí informaci, zda je studie ve stavu pre-launched. """
        return self.status == constants.STUDY_STATUS_PRELAUNCH

    def is_in_progress(self):
        """ Vrátí informaci, zda je studie ve stavu progress. """
        return self.status == constants.STUDY_STATUS_PROGRESS

    def is_payment_method_allowed(self, payment_method: str) -> bool:
        if payment_method == core_constants.PAYMENT_TYPE_BANK_TRANSFER:
            return self.bank_transfer
        elif payment_method == core_constants.PAYMENT_TYPE_POST_OFFICE:
            return self.post_office_cash
        else:
            raise NotImplementedError('this payment method is not implemented')

    def _make_after_draft(self):
        pass

    def _make_after_prelaunch(self):
        self.prelaunched_at = timezone.now()

    def _make_after_progress(self):
        self.progress_at = timezone.now()

    def _make_after_billing(self):
        self.billing_at = timezone.now()

    def _make_after_closed(self):
        self.closed_at = timezone.now()

    def save(self, *args, **kwargs):
        if self._status != self.status:
            # zavolám funkci _make_after_X ... abych si denormaliozval potřebná data
            getattr(self, '_make_after_{}'.format(str(self.status).lower()))()
        super(Study, self).save(*args, **kwargs)

    @property
    def sazka_transfer(self):
        return False

    def get_sponsor_name(self):
        return self.sponsor_name if self.is_cro_operator() else self.company.name

    def is_cro_operator(self) -> bool:
        return self.operator == constants.STUDY_OPERATOR_CRO
