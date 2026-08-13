from django.contrib import admin
from .models import FamilyMember

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'relation', 'user', 'date_of_birth')
    list_filter = ('relation', 'gender')
    search_fields = ('name', 'user__username')
