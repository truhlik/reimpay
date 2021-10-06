from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = [
            # 'email',
            'subject',
            'text',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['user'] = user
            validated_data['email'] = user.email
        return super(TicketSerializer, self).create(validated_data)
