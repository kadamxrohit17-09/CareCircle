from rest_framework import serializers
from .models import MedicalReport, LabResult

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'

class MedicalReportSerializer(serializers.ModelSerializer):
    lab_results = LabResultSerializer(many=True, read_only=True)

    class Meta:
        model = MedicalReport
        fields = '__all__'
        read_only_fields = ('analysis_status', 'created_at', 'updated_at', 'uploaded_at', 'report_type', 'report_date')
