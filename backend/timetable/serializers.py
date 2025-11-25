"""
Serializers for timetable app.
"""
from rest_framework import serializers
from .models import Room, TimeSlot, Timetable, ScheduleGenerationLog
from accounts.serializers import CourseSerializer, UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    """Room serializer."""
    class Meta:
        model = Room
        fields = '__all__'


class TimeSlotSerializer(serializers.ModelSerializer):
    """Time slot serializer."""
    class Meta:
        model = TimeSlot
        fields = '__all__'


class TimetableSerializer(serializers.ModelSerializer):
    """Timetable serializer."""
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    teacher = UserSerializer(read_only=True)
    teacher_id = serializers.IntegerField(write_only=True)
    room = RoomSerializer(read_only=True)
    room_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    time_slot = TimeSlotSerializer(read_only=True)
    time_slot_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Timetable
        fields = '__all__'
        read_only_fields = ('created_at',)


class ScheduleGenerationLogSerializer(serializers.ModelSerializer):
    """Schedule generation log serializer."""
    class Meta:
        model = ScheduleGenerationLog
        fields = '__all__'
        read_only_fields = ('generated_at',)

