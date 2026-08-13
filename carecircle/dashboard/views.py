from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from family.models import FamilyMember
from reports.models import MedicalReport, LabResult
from reminders.models import FollowUp

class DashboardView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        members_count = FamilyMember.objects.filter(user=user).count()
        reports = MedicalReport.objects.filter(member__user=user)
        total_reports = reports.count()
        analyzed_reports = reports.filter(analysis_status='completed').count()
        
        flagged_results = LabResult.objects.filter(
            report__member__user=user,
            status__in=['high', 'low', 'borderline']
        ).count()
        
        upcoming_followups = FollowUp.objects.filter(
            member__user=user,
            completed=False
        ).order_by('follow_up_date')[:5].values('id', 'description', 'follow_up_date', 'member__name')
        
        recent_reports = reports.order_by('-uploaded_at')[:5].values('id', 'title', 'uploaded_at', 'member__name', 'analysis_status')

        return Response({
            'family_members': members_count,
            'total_reports': total_reports,
            'analyzed_reports': analyzed_reports,
            'flagged_results': flagged_results,
            'upcoming_followups': list(upcoming_followups),
            'recent_reports': list(recent_reports),
        })
