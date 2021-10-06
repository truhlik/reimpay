from django_filters import FilterSet, UUIDFilter, NumberFilter, BooleanFilter, ChoiceFilter
from . import models


class PatientVisitItemFilter(FilterSet):
    BOOLEAN_CHOICES = (('true', 'true'), ('false', 'false'), ('none', 'none'), ('any', 'any'))
    approved = ChoiceFilter(choices=BOOLEAN_CHOICES, method='approved_filter')
    study_id = UUIDFilter(field_name='patient_visit__study_id')

    class Meta:
        model = models.PatientVisitItem
        fields = ('approved', 'study_id', 'patient_visit__patient__site__id', 'patient_visit__patient__id',
                  'payment_status', 'patient_visit')

    def approved_filter(self, queryset, name, value):
        if value == 'true':
            return queryset.approved()
        elif value == 'false':
            return queryset.rejected()
        elif value == 'none':
            return queryset.not_processed()
        elif value == 'any':
            return queryset.processed()
        return queryset


class PatientFilter(FilterSet):
    change_payment = BooleanFilter(method='change_filter')
    active = BooleanFilter(method='active_filter')
    study_id = UUIDFilter()
    site_id = NumberFilter()

    class Meta:
        model = models.Patient
        fields = ('active', 'study_id', 'site_id', 'change_payment')

    def active_filter(self, queryset, name, value):
        if value is True:
            return queryset.in_progress()
        return queryset

    def change_filter(self, queryset, name, value):
        if value is True:
            return queryset.flagged()
        elif value is False:
            return queryset.not_flagged()
        return queryset
