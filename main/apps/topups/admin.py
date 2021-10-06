from django.contrib import admin

from .models import TopUp


@admin.register(TopUp)
class TopUpAdmin(admin.ModelAdmin):
    list_display = ['study', 'amount']
