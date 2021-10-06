from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponse

from .models import Payment, PaycheckGeneration, PostOfficeFile
from .services.post_office_export import PostOfficeFileExportService
from .utils import generate_transfer_operational_cp


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['total_value_round', 'created_at', 'url', 'variable_symbol', 'specific_symbol',
                    'constant_symbol', 'returned_on']
    list_filter = ['constant_symbol']
    search_fields = ['variable_symbol']

    def total_value_round(self, obj):
        return obj.total_value / settings.INT_RATIO


@admin.register(PaycheckGeneration)
class PaycheckGenerationAdmin(admin.ModelAdmin):
    list_display = ['study', 'created_at']
    list_filter = ['study']


@admin.register(PostOfficeFile)
class PostOfficeFileAdmin(admin.ModelAdmin):
    list_display = ['updated_at', 'created_at']
    list_filter = ['created_at']

    def download_post_office_vds(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, 'You must choose only 1 item.', messages.ERROR)

        if len(queryset) == 0:
            self.message_user(request, 'You must choose 1 item.', messages.ERROR)

        payments_qs = Payment.objects.filter(post_office=queryset[0])

        svc = PostOfficeFileExportService(payments_qs)
        txt = svc.perform()

        # musím ještě vytvořit převod z operačního účtu na ČP
        generate_transfer_operational_cp(svc.get_total_fee_price() / 100, svc.get_variable_symbol())

        response = HttpResponse(txt, content_type="application/text")
        response['Content-Disposition'] = 'attachment; filename={0}'.format('export.txt')
        return response

    actions = [download_post_office_vds]
