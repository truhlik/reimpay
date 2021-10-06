from django.contrib import admin

from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['company', 'invoice_number', 'amount', 'status', 'fakturoid_public_url']
    list_filter = ['status', 'company']
    search_fields = ['invoice_number', 'company']
