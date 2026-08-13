from django.contrib import admin
from .models import FollowUp

@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('description', 'member', 'follow_up_date', 'completed', 'source')
    list_filter = ('completed', 'source')
    search_fields = ('description', 'member__name')
