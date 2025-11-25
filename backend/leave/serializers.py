"""
Serializers for leave app.
"""
from rest_framework import serializers
from .models import LeaveRequest, LeaveAnalytics
from accounts.serializers import UserSerializer


class LeaveRequestSerializer(serializers.ModelSerializer):
    """Leave request serializer."""
    student = UserSerializer(read_only=True)
    approved_by_name = serializers.SerializerMethodField()
    duration_days = serializers.SerializerMethodField()
    
    class Meta:
        model = LeaveRequest
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'student', 'approved_by')
    
    def get_approved_by_name(self, obj):
        return f"{obj.approved_by.first_name} {obj.approved_by.last_name}" if obj.approved_by else None
    
    def get_duration_days(self, obj):
        return obj.duration_days


class LeaveAnalyticsSerializer(serializers.ModelSerializer):
    """Leave analytics serializer."""
    student = UserSerializer(read_only=True)
    
    class Meta:
        model = LeaveAnalytics
        fields = '__all__'

