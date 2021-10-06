from django.conf import settings
from django.contrib import admin

from .models import CreditBalance


@admin.register(CreditBalance)
class CreditBalanceAdmin(admin.ModelAdmin):
    list_display = ['study', 'balance_amount_round', 'balance_sum_round', 'balance_type']
    list_filter = ['balance_type']

    def balance_amount_round(self, obj):
        return obj.balance_amount / settings.INT_RATIO

    def balance_sum_round(self, obj):
        return obj.balance_sum / settings.INT_RATIO
