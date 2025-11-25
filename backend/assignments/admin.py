"""
Admin for assignments app.
"""
from django.contrib import admin
from .models import Assignment, Submission, DeadlineNotification


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'deadline', 'max_marks', 'submission_count')
    list_filter = ('course', 'teacher', 'deadline')
    search_fields = ('title', 'course__code')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'marks_obtained', 'is_graded', 'is_late')
    list_filter = ('is_graded', 'submitted_at', 'assignment__course')
    search_fields = ('student__email', 'assignment__title')
    readonly_fields = ('submitted_at', 'updated_at')


@admin.register(DeadlineNotification)
class DeadlineNotificationAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'reminder_type', 'reminder_sent_at')
    list_filter = ('reminder_type', 'reminder_sent_at')

