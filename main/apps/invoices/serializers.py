from rest_framework import serializers

from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = [
            'id',
            'company',
            'fakturoid_public_url',
            'invoice_number',
            'issue_date',
            'amount',
            'status',
        ]
