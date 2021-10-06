from rest_framework import viewsets, mixins

from main.libraries.permissions import HasCompanyPermission
from . import serializers
from .models import AuditLog


class HistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = AuditLog.objects.all().select_related('content_type', 'user').order_by('-created_at')
    permission_classes = [HasCompanyPermission]
    serializer_class = serializers.AuditLogSerializer
    filterset_fields = ['study_id']
