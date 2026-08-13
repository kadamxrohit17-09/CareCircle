from django.db import models
from family.models import FamilyMember
from reports.models import MedicalReport

class FollowUp(models.Model):
    SOURCE_CHOICES = (
        ('doctor_instruction', 'Doctor Instruction'),
        ('report_instruction', 'Report Instruction'),
        ('manual', 'Manual'),
    )

    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='follow_ups')
    report = models.ForeignKey(MedicalReport, on_delete=models.SET_NULL, null=True, blank=True, related_name='follow_ups')
    follow_up_date = models.DateField()
    description = models.TextField()
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='manual')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} on {self.follow_up_date} ({self.member.name})"
