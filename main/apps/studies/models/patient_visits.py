from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


from simple_history.models import HistoricalRecords

from main.libraries.models import BaseModel, SimpleModel
from ..managers import PatientVisitItemQuerySet, PatientVisitQuerySet
from .. import constants
from ..signals import approved


class PatientVisitItem(BaseModel):
    objects = PatientVisitItemQuerySet.as_manager()

    patient_visit = models.ForeignKey('studies.PatientVisit', related_name='patient_visit_items', on_delete=models.CASCADE)
    visit_item = models.ForeignKey('studies.VisitItem', related_name='patient_visit_items', on_delete=models.CASCADE)
    approved = models.NullBooleanField(_('approved'), default=None)
    origin = models.CharField(_('origin'), choices=constants.STUDY_PATIENT_VISIT_ITEM_ORIGIN_CHOICES, max_length=64,
                              default=constants.STUDY_PATIENT_VISIT_ITEM_ORIGIN_CRA)
    reject_reason = models.TextField(_('reject reason'), blank=True, null=True)
    note_cra = models.TextField(_('note cra'), blank=True, null=True)
    payment_status = models.CharField(max_length=32, choices=constants.STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_CHOICES,
                                      null=True, default=constants.STUDY_PATIENT_VISIT_ITEM_PAYMENT_STATUS_WAITING)

    class Meta:
        verbose_name = 'patient visit item'
        verbose_name_plural = _('patient visit items')

    def __init__(self, *args, **kwargs):
        super(PatientVisitItem, self).__init__(*args, **kwargs)
        self._approved = self.approved

    def approved_was_changed(self):
        return self.approved != self._approved

    def is_owner(self, user):
        # vlastník položky musí přesně odpovídat vlastíkovi celé visity
        return self.patient_visit.is_owner(user)

    def should_send_approved_signal(self):
        return (self.approved_was_changed() or self._state.adding) and self.approved is True

    @property
    def status(self) -> str:
        """ Vrátí textový status tohoto reimu. V případě, že je approved, tak vracím status platby. """
        if self.approved is None:
            return 'WAITING FOR CRA APPROVAL'
        elif self.approved is False:
            return 'REJECTED'
        else:
            return self.get_payment_status_display()

    def save(self, *args, **kwargs):
        super(PatientVisitItem, self).save(*args, **kwargs)

        if self.should_send_approved_signal():
            approved.send(sender=self.__class__, instance=self)
            self.patient_visit.d_reim_approved = True
            self.patient_visit.save()


class PatientVisit(SimpleModel):
    objects = PatientVisitQuerySet.as_manager()

    study = models.ForeignKey('studies.Study', verbose_name=_('study'), related_name='patient_visits', on_delete=models.CASCADE)
    patient = models.ForeignKey('studies.Patient', verbose_name=_('patient'), related_name='patient_visits', on_delete=models.CASCADE)
    visit = models.ForeignKey('studies.Visit', verbose_name=_('visit'), related_name='patient_visits', on_delete=models.CASCADE)
    visit_items = models.ManyToManyField('studies.VisitItem', related_name='patient_visits', through=PatientVisitItem, blank=True)

    visit_date = models.DateField('visit date')

    d_reim_approved = models.BooleanField(default=False)

    history = HistoricalRecords(excluded_fields=['created_at', 'updated_at', 'd_reim_approved'])

    class Meta:
        verbose_name = _('patient visit')
        verbose_name_plural = _('patient visits')

    def is_owner(self, user):
        if user.is_anonymous:
            return False
        # admin je vlastníkem vždycky pokud je vlastníkem studie
        elif user.has_admin_role():
            return self.study.is_owner(user)
        # cra je vlastníkem, pokud je vlastníkem pacienta
        return self.patient.is_owner(user)

    def clean(self):
        super(PatientVisit, self).clean()

        if self.patient and self.study and self.patient.study_id != self.study.id:
            raise ValidationError('InconsistentData: patient.study is not the same as study')

        if self.visit and self.study and self.visit.study_id != self.study.id:
            raise ValidationError('InconsistentData: visit.study is not the same as study')

        if self.patient and self.visit and self.patient.study_id != self.visit.study_id:
            raise ValidationError('InconsistentData: visit.study is not the same as patient.study')

        if self.visit and self.visit_items.all():
            for item in self.visit_items.all():
                if item.visit_id != self.visit_id:
                    raise ValidationError('InconsistentData: visit is not the same as visit_items.study')

        return

    def get_group_obj_id(self):
        return self.study_id

    def _get_visit_from_visit_items(self):
        for v in self.visit_items.all():
            return v.visit
        return None

    def save(self, *args, **kwargs):
        if self.study_id is None:
            self.study_id = self.patient.study_id
        if self.visit_date is None:
            self.visit_date = timezone.now().date()
        if self.visit_id is None:
            self.visit = self._get_visit_from_visit_items()
        if self.visit.visit_type == constants.STUDY_VISIT_TYPE_DISCONTINUAL:
            from ..utils import set_patient_terminated
            set_patient_terminated(self.patient)
        super(PatientVisit, self).save(*args, **kwargs)
