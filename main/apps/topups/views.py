import datetime

from django.views.generic.detail import SingleObjectMixin
from rest_framework import viewsets, mixins
from constance import config

from main.libraries.permissions import IsCraOrAdmin
from main.libraries.serializers.mixins import GetSerializerClassMixin
from . import models, serializers
from main.libraries.views import ApiPdfTemplateView


class TopUpViewSet(GetSerializerClassMixin, mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.TopUp.objects.all()
    permission_classes = [IsCraOrAdmin]
    serializer_class = serializers.TopUpSerializer
    filterset_fields = ['study_id']

    def get_queryset(self):
        return super(TopUpViewSet, self).get_queryset().owner(self.request.user)


class TopUpPDF(SingleObjectMixin, ApiPdfTemplateView):
    permission_classes = [IsCraOrAdmin]
    filename = 'my_pdf.pdf'
    template_name = 'topups/topup_request.html'
    cmd_options = {
        'margin-top': 3,
    }

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return models.TopUp.objects.none()
        return models.TopUp.objects.owner(self.request.user)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(TopUpPDF, self).get(request, *args, **kwargs)

    def get_filename(self):
        return "topup_{}_{}.pdf".format(self.object.id, datetime.date.today().strftime('%Y-%m-%d'))

    def get_context_data(self, **kwargs):
        ctx = super(TopUpPDF, self).get_context_data(**kwargs)
        ctx.update({
            'config': config,
        })
        return ctx
