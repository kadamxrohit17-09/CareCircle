from rest_framework import viewsets
from .models import FollowUp
from .serializers import FollowUpSerializer

class FollowUpViewSet(viewsets.ModelViewSet):
    serializer_class = FollowUpSerializer

    def get_queryset(self):
        return FollowUp.objects.filter(member__user=self.request.user)
