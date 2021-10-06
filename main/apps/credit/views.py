from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from main.libraries.permissions import IsCraOrAdmin
from main.libraries.serializers.mixins import GetSerializerClassMixin
from . import models, serializers, utils
from ..core.swagger import path_id_param_int


class CreditBalanceFilter(FilterSet):

    class Meta:
        model = models.CreditBalance
        fields = {
            'created_at': ('date__lte', 'date__gte'),
            'study_id': ('exact', ),
        }


@method_decorator(name='retrieve', decorator=path_id_param_int)
class CreditBalanceViewSet(GetSerializerClassMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.CreditBalance.objects.all()
    permission_classes = [IsAuthenticated, IsCraOrAdmin]
    filterset_fields = ['study_id']
    filter_backends = (DjangoFilterBackend,)
    filter_class = CreditBalanceFilter
    serializer_class = serializers.CreditBalanceSerializer

    def get_queryset(self):
        return super(CreditBalanceViewSet, self).get_queryset().owner(self.request.user).order_by('-created_at')

    @action(methods=['GET'], detail=False)
    def export(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        utils.get_csv_export(response, queryset)
        return response
