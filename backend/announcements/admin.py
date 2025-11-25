"""
Admin for announcements app.
"""
from django.contrib import admin
from .models import Announcement, Notification


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'priority', 'target_audience', 'is_pinned', 'created_at')
    list_filter = ('priority', 'target_audience', 'is_pinned', 'created_at')
    search_fields = ('title', 'content', 'author__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__email', 'title', 'message')

