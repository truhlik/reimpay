from django.utils.decorators import method_decorator
from rest_framework import viewsets

from main.libraries.permissions import IsAdmin
from main.libraries.serializers.mixins import GetSerializerClassMixin
from . import models, serializers
from ..core.swagger import path_id_param_int


@method_decorator(name='retrieve', decorator=path_id_param_int)
class InvoiceViewSet(GetSerializerClassMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Invoice.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = serializers.InvoiceSerializer

    def get_queryset(self):
        return super(InvoiceViewSet, self).get_queryset().owner(self.request.user).order_by('-created_at')
