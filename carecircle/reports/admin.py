from django.contrib import admin
from .models import MedicalReport, LabResult

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'member', 'report_date', 'analysis_status', 'uploaded_at')
    list_filter = ('analysis_status', 'report_type')
    search_fields = ('title', 'member__name')

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'value', 'unit', 'status', 'report')
    list_filter = ('status',)
    search_fields = ('test_name', 'report__title')
