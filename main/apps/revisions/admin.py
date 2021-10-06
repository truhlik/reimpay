from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'study', 'user', 'content_type', 'obj_name', 'action']
    list_filter = ['action']
