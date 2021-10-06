from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'web', 'reg_number', 'vat_number', 'get_address']
    search_fields = ['name', 'email', 'get_address', 'reg_number']

    def get_address(self, obj):
        return obj.address
