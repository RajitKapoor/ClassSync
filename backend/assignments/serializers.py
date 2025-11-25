"""
Serializers for assignments app.
"""
from rest_framework import serializers
from .models import Assignment, Submission, DeadlineNotification
from accounts.serializers import CourseSerializer, UserSerializer


class AssignmentSerializer(serializers.ModelSerializer):
    """Assignment serializer."""
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    teacher_name = serializers.SerializerMethodField()
    submission_count = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'teacher')
    
    def get_teacher_name(self, obj):
        return f"{obj.teacher.first_name} {obj.teacher.last_name}" if obj.teacher else None
    
    def get_submission_count(self, obj):
        return obj.submission_count
    
    def get_is_overdue(self, obj):
        return obj.is_overdue


class SubmissionSerializer(serializers.ModelSerializer):
    """Submission serializer."""
    assignment = AssignmentSerializer(read_only=True)
    assignment_id = serializers.IntegerField(write_only=True)
    student = UserSerializer(read_only=True)
    is_late = serializers.SerializerMethodField()
    
    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('submitted_at', 'updated_at', 'student')
    
    def get_is_late(self, obj):
        return obj.is_late


class DeadlineNotificationSerializer(serializers.ModelSerializer):
    """Deadline notification serializer."""
    class Meta:
        model = DeadlineNotification
        fields = '__all__'

