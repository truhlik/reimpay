from django.contrib import admin

from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'subject', 'sent_at']
    list_filter = ['sent_at']
