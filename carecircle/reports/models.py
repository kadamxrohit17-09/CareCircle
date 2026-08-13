from django.db import models
from family.models import FamilyMember

class MedicalReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='reports')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='reports/')
    report_type = models.CharField(max_length=100, blank=True)
    report_date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    analysis_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.member.name}"

class LabResult(models.Model):
    STATUS_CHOICES = (
        ('normal', 'Normal'),
        ('borderline', 'Borderline'),
        ('low', 'Low'),
        ('high', 'High'),
        ('unknown', 'Unknown'),
    )

    report = models.ForeignKey(MedicalReport, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=255)
    value = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, blank=True)
    reference_range = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unknown')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name}: {self.value} {self.unit} ({self.status})"
