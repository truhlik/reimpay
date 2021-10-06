from django_filters import FilterSet, UUIDFilter, ChoiceFilter
from . import models
from .constants import USER_ROLE_CHOICES


class UserStudyFilter(FilterSet):
    study_id = UUIDFilter(field_name='sites__study__id')
    role = ChoiceFilter(choices=USER_ROLE_CHOICES)

    class Meta:
        model = models.User
        fields = ('role', 'study_id')
