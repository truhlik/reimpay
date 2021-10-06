from django.conf import settings
from rest_framework import serializers

from .models import CreditBalance


class MoneyField(serializers.CharField):

    def to_representation(self, value):
        return "{} CZK".format(float(value) / settings.INT_RATIO)


class CreditBalanceSerializer(serializers.ModelSerializer):
    balance_amount = MoneyField()

    class Meta:
        model = CreditBalance
        fields = ['id', 'balance_type', 'balance_amount', 'created_at']
