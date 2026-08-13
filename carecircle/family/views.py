from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FamilyMember
from .serializers import FamilyMemberSerializer

class FamilyMemberViewSet(viewsets.ModelViewSet):
    serializer_class = FamilyMemberSerializer

    def get_queryset(self):
        return FamilyMember.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        member = self.get_object()
        events = []
        
        for report in member.reports.all():
            events.append({
                'date': report.uploaded_at.strftime('%Y-%m-%d'),
                'type': 'report_upload',
                'title': report.title,
                'description': 'Medical report uploaded'
            })
            if report.analysis_status == 'completed':
                events.append({
                    'date': report.updated_at.strftime('%Y-%m-%d'),
                    'type': 'report_analyzed',
                    'title': f"{report.title} Analyzed",
                    'description': 'AI finished analyzing the report'
                })
        
        for followup in member.follow_ups.all():
            events.append({
                'date': followup.follow_up_date.strftime('%Y-%m-%d'),
                'type': 'follow_up',
                'title': 'Follow-up' if not followup.completed else 'Completed Follow-up',
                'description': followup.description
            })
            
        events.sort(key=lambda x: x['date'], reverse=True)
        return Response(events)
