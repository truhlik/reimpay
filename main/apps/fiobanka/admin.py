from django.contrib import admin

from .models import FiobankTransactions


@admin.register(FiobankTransactions)
class FiobankTransactionsAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'variable_symbol', 'amount', 'processed_on']
