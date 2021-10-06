from django.urls import reverse
from rest_framework import serializers

from main.apps.topups.models import TopUp


class TopUpSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(min_value=999)
    file = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TopUp
        fields = ['created_at', 'study', 'amount', 'file']

    def get_file(self, obj):
        request = self.context['request']
        return request.build_absolute_uri(reverse('topup-pdf', args=(obj.id, )))
