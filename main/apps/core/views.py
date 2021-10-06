import urllib

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django_cron import get_class
from django_cron.management.commands.runcrons import run_cron_with_cache_check
from rest_framework import viewsets, mixins, views, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from main.libraries.permissions import IsCraOrAdmin
from . import serializers
from . import utils
from .swagger import path_id_param_str
from ..studies.models import Study
from ..studies import utils as study_utils
from ...libraries.serializers.mixins import GetSerializerClassMixin


@method_decorator(name='retrieve', decorator=path_id_param_str)
@method_decorator(name='stats', decorator=path_id_param_str)
class StudyCreditInfoViewSet(GetSerializerClassMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Study.objects.active()
    permission_classes = [IsCraOrAdmin]
    serializer_class = serializers.CreditInfoSerializer
    serializer_action_classes = {
        'retrieve': serializers.CreditInfoSerializer,
        'stats': serializers.StudyStatSerializer,
    }

    def get_queryset(self):
        return super(StudyCreditInfoViewSet, self).get_queryset().list(self.request.user).order_by('-created_at')

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        actual_balance = utils.get_actual_balance(instance)
        paid = utils.get_paid(instance)
        remaining_visits = study_utils.get_remaining_visits(instance)
        avg_visit_value = int(study_utils.get_avg_visit_value(instance))
        exp_budget_need = remaining_visits * avg_visit_value

        return Response({
            'actual_balance': "{} CZK".format(int(actual_balance / settings.INT_RATIO)),
            'paid': "{} CZK".format(int(paid / settings.INT_RATIO)),
            'remaining_visits': "{}".format(remaining_visits),
            'avg_visit_value': "{} CZK".format(int(avg_visit_value)),
            'exp_budget_need': "{} CZK".format(int(exp_budget_need)),
        })

    @action(methods=['GET'], detail=True, serializer_class=serializers.StudyStatSerializer)
    def stats(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DoctorLoginView(views.APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, *args, **kwargs):
        serializer = serializers.DoctorLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.validated_data['patient']

        # uložím si do sessions informaci, že k tomuto pacientovi má přístup 30min.
        try:
            dct = request.session[settings.DOCTOR_SESSION_KEY]
            dct[patient.id] = (timezone.now() + timezone.timedelta(minutes=settings.DOCTOR_SESSION_MIN)).isoformat()
            request.session[patient.id] = dct
        except KeyError:
            dct = {
                patient.id: (timezone.now() + timezone.timedelta(minutes=settings.DOCTOR_SESSION_MIN)).isoformat()
            }
            request.session[settings.DOCTOR_SESSION_KEY] = dct

        return JsonResponse({'redirect_to': urllib.parse.unquote(reverse('frontend-patient-detail',
                                                                         args=(patient.id, )))})


def run_cron_view(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('unsupported HTTP method')

    cron_class_names = getattr(settings, 'CRON_CLASSES', [])
    crons_to_run = [get_class(x) for x in cron_class_names]

    for cron_class in crons_to_run:
        run_cron_with_cache_check(
            cron_class,
            force=True,
            silent=False,
        )
    messages.success(request, 'cron successfully started')
    return HttpResponseRedirect(reverse('admin:django_cron_cronjoblog_changelist'))
