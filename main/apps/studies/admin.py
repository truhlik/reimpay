from django.contrib import admin

from .models import Study, StudyItem, Arm, Site, Patient, PatientVisitItem, Visit, VisitItem, PatientVisit


@admin.register(Study)
class StudyAdmin(admin.ModelAdmin):
    list_display = ['number', 'identifier', 'status', 'bank_transfer', 'post_office_cash', 'pay_frequency', 'company']
    list_filter = ['status']
    search_fields = ['title', 'description']


@admin.register(StudyItem)
class StudyItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'deleted', 'study']
    list_filter = ['deleted']
    search_fields = ['title', 'description']


@admin.register(Arm)
class ArmAdmin(admin.ModelAdmin):
    list_display = ['title', 'study', 'max_unscheduled']
    search_fields = ['title']


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ['title', 'study', 'expected_patients', 'cra']
    search_fields = ['title']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['number', 'payment_type', 'payment_info', 'name', 'study', 'arm']
    search_fields = ['title']
    list_filter = ['status', 'payment_type']


@admin.register(Visit)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['title', 'study', 'arm', 'visit_type', 'deleted']
    search_fields = ['title']
    list_filter = ['deleted', 'visit_type']


@admin.register(VisitItem)
class VisitItemAdmin(admin.ModelAdmin):
    list_display = ['visit', 'study_item', 'deleted']
    list_filter = ['deleted']


@admin.register(PatientVisitItem)
class PatientVisitItemAdmin(admin.ModelAdmin):
    list_display = ['patient_visit', 'visit_item', 'approved', 'origin']
    list_filter = ['approved', 'origin']


@admin.register(PatientVisit)
class PatientVisitAdmin(admin.ModelAdmin):
    list_display = ['patient', 'visit', 'study', 'visit_date']

