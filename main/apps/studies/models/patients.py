from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from encrypted_fields import fields
from simple_history.models import HistoricalRecords

from main.apps.core.constants import PAYMENT_TYPE_CHOICES
from main.libraries.models import BaseModel
from ..managers import PatientQuerySet
from .. import constants


class Patient(BaseModel):
    objects = PatientQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', verbose_name=_('study'), related_name='patients', on_delete=models.CASCADE)
    arm = models.ForeignKey('studies.Arm', verbose_name=_('arm'), related_name='patients', on_delete=models.CASCADE)
    site = models.ForeignKey('studies.Site', verbose_name=_('site'), related_name='patients', on_delete=models.CASCADE)

    status = models.CharField('status', choices=constants.STUDY_PATIENT_STATUS_CHOICES, max_length=64,
                              default=constants.STUDY_PATIENT_STATUS_ACTIVE)
    number = models.CharField(_('randomisation'), max_length=255)

    change_payment_request = models.DateTimeField(blank=True, null=True)
    payment_type = models.CharField(_('payment form'), choices=PAYMENT_TYPE_CHOICES, max_length=32)
    payment_info = fields.EncryptedCharField(_('payment info'), max_length=255, blank=True, null=True)
    # pro platbu slozenkou
    name = fields.EncryptedCharField(_('name'), max_length=255, blank=True, null=True)
    street = fields.EncryptedCharField(_('street'), max_length=255, blank=True, null=True)
    street_number = fields.EncryptedCharField(_('street_number'), max_length=255, blank=True, null=True)
    city = fields.EncryptedCharField(_('city'), max_length=255, blank=True, null=True)
    zip = fields.EncryptedCharField(_('zip'), max_length=255, blank=True, null=True)

    deleted = models.BooleanField(default=False)

    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at'])

    class Meta:
        verbose_name = _('patient')
        verbose_name_plural = _('patients')
        unique_together = (('study', 'number'), )

    def __str__(self):
        return self.number

    def is_owner(self, user):
        if user.is_anonymous:
            return False
        if user.has_admin_role():
            return self.study.is_owner(user)
        return self.site.cra == user

    def clean(self):
        super(Patient, self).clean()

        if self.arm is None or self.study is None or self.site is None:
            return

        if self.arm.study_id != self.study.id:
            raise ValidationError('InconsistentData: arm.study is not the same as study')

        if self.site.study_id != self.study.id:
            raise ValidationError('InconsistentData: arm.study is not the same as study')
        return

    def get_group_obj_id(self):
        return self.study_id

    @cached_property
    def next_visit(self):
        """ Vrátí následující visitu pro pacienta. """
        from .. import utils
        return utils.get_next_patient_visit(self)

    @cached_property
    def _payment_data(self):
        return self.payments_data.all().order_by('-created_at').first()

    def _should_normalize_payment_data(self):
        """
        Vrátí zda je potřeba vytvořit normalizovaný objekt pro payment data.
        Porovnáná aktuální data s nejnovějšíma vytvořenýma.
        """

        if self._payment_data is None:
            return True

        self_data = {
            'payment_type': self.payment_type,
            'payment_info': self.payment_info,
            'name': self.name,
            'street': self.payment_type,
            'city': self.city,
            'zip': self.zip,
        }

        normalized_data = {
            'payment_type': self._payment_data.payment_type,
            'payment_info': self._payment_data.payment_info,
            'name': self._payment_data.name,
            'street': self._payment_data.payment_type,
            'city': self._payment_data.city,
            'zip': self._payment_data.zip,
        }
        return self_data != normalized_data

    def _create_payment_data(self):
        pd = PatientPaymentData(
            patient=self,
            payment_type=self.payment_type,
            payment_info=self.payment_info,
            name=self.name,
            street=self.street,
            city=self.city,
            zip=self.zip,
        )
        pd.save()
        return pd

    def patient_visit_items(self):
        from main.apps.studies.models import PatientVisitItem
        return PatientVisitItem.objects.filter(patient_visit__patient=self)

    def save(self, *args, **kwargs):
        if self.study_id is None:
            self.study_id = self.site.study_id

        super(Patient, self).save(*args, **kwargs)
        if self._should_normalize_payment_data():
            self._payment_data = self._create_payment_data()
            self.change_payment_request = None
            self.save()

    @property
    def visits_count(self):
        return len(self.patient_visits.all())

    def next_visits(self):
        from .. import utils
        qs = utils.get_patient_available_visits(self)
        qs = qs.prefetch_related('visit_items__study_item')
        return qs


class PatientPaymentData(BaseModel):
    """ Složí pouze pro denormalizaci payment dat Pacienta. """
    patient = models.ForeignKey('studies.Patient', on_delete=models.CASCADE, related_name='payments_data')

    payment_type = models.CharField(_('payment form'), choices=PAYMENT_TYPE_CHOICES, max_length=32)
    payment_info = fields.EncryptedCharField(_('payment info'), max_length=255, blank=True, null=True)

    name = fields.EncryptedCharField(_('name'), max_length=255, blank=True, null=True)
    street = fields.EncryptedCharField(_('street'), max_length=255, blank=True, null=True)
    city = fields.EncryptedCharField(_('city'), max_length=255, blank=True, null=True)
    zip = fields.EncryptedCharField(_('zip'), max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
