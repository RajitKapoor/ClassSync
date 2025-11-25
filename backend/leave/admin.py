"""
Admin for leave app.
"""
from django.contrib import admin
from .models import LeaveRequest, LeaveAnalytics


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'leave_type', 'start_date', 'end_date', 'status', 'approved_by', 'created_at')
    list_filter = ('status', 'leave_type', 'start_date', 'created_at')
    search_fields = ('student__email', 'reason')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_leaves', 'reject_leaves']
    
    def approve_leaves(self, request, queryset):
        queryset.update(status='approved', approved_by=request.user)
    approve_leaves.short_description = "Approve selected leaves"
    
    def reject_leaves(self, request, queryset):
        queryset.update(status='rejected', approved_by=request.user)
    reject_leaves.short_description = "Reject selected leaves"


@admin.register(LeaveAnalytics)
class LeaveAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('student', 'year', 'total_leaves', 'approved_leaves', 'rejected_leaves', 'total_days')
    list_filter = ('year',)

