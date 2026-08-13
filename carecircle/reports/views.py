from django.db import transaction
from rest_framework import viewsets, mixins, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MedicalReport, LabResult
from .serializers import MedicalReportSerializer
from ai_analysis.services import analyze_report
from reminders.models import FollowUp

class MedicalReportViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalReportSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    def get_queryset(self):
        return MedicalReport.objects.filter(member__user=self.request.user)

    @action(detail=True, methods=['post'], url_path='analyze')
    def analyze(self, request, pk=None):
        report = self.get_object()
        
        if report.analysis_status == 'completed':
            return Response({'success': False, 'message': 'Report is already analyzed'})

        report.analysis_status = 'processing'
        report.save()

        # Call AI service
        mime_type = 'application/pdf' if report.file.name.endswith('.pdf') else 'image/jpeg'
        if report.file.name.endswith('.png'):
            mime_type = 'image/png'

        success, data = analyze_report(report.file.path, mime_type)
        
        if not success:
            report.analysis_status = 'failed'
            report.save()
            return Response({'success': False, 'message': data}, status=400)
            
        try:
            with transaction.atomic():
                # Save extracted fields to report
                report.report_type = data.get('report_type', '')
                if data.get('report_date'):
                    report.report_date = data.get('report_date')
                
                # Save Lab Results
                for res in data.get('results', []):
                    LabResult.objects.create(
                        report=report,
                        test_name=res.get('test_name', ''),
                        value=res.get('value', ''),
                        unit=res.get('unit', ''),
                        reference_range=res.get('reference_range', ''),
                        status=res.get('status', 'unknown')
                    )
                
                # Save FollowUp
                follow_up_data = data.get('follow_up')
                if follow_up_data and follow_up_data.get('date'):
                    FollowUp.objects.create(
                        member=report.member,
                        report=report,
                        follow_up_date=follow_up_data['date'],
                        description=follow_up_data.get('instruction', 'Follow-up appointment'),
                        source=follow_up_data.get('source', 'report_instruction')
                    )
                
                report.analysis_status = 'completed'
                report.save()
            
            return Response({'success': True, 'message': 'Analysis complete', 'data': data})
        except Exception as e:
            report.analysis_status = 'failed'
            report.save()
            return Response({'success': False, 'message': f"Failed to save results: {str(e)}"}, status=400)
