from rest_framework import serializers

from main.apps.revisions.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)
    content_type = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'user',
            'created_at',
            'content_type',
            'update_data',
            'action',
            'obj_name',
        ]


