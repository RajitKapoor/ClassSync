"""
Serializers for announcements app.
"""
from rest_framework import serializers
from .models import Announcement, Notification
from accounts.serializers import UserSerializer, CourseSerializer


class AnnouncementSerializer(serializers.ModelSerializer):
    """Announcement serializer."""
    author = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'author')


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer."""
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('created_at',)

