"""
Timetable and schedule models.
"""
from django.db import models
from accounts.models import User, Course, Department


class Room(models.Model):
    """Room model."""
    name = models.CharField(max_length=50, unique=True)
    capacity = models.IntegerField()
    building = models.CharField(max_length=100, blank=True)
    facilities = models.TextField(blank=True)  # e.g., "projector, whiteboard"
    
    class Meta:
        db_table = 'rooms'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.capacity} seats)"


class TimeSlot(models.Model):
    """Time slot model."""
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        db_table = 'time_slots'
        unique_together = ['day', 'start_time', 'end_time']
        ordering = ['day', 'start_time']
    
    def __str__(self):
        return f"{self.get_day_display()} {self.start_time} - {self.end_time}"


class Timetable(models.Model):
    """Timetable entry model."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetable_entries')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timetable_entries', limit_choices_to={'role': 'teacher'})
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='timetable_entries')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='timetable_entries')
    semester = models.IntegerField(default=1)
    academic_year = models.CharField(max_length=20, default='2024-2025')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'timetable'
        indexes = [
            models.Index(fields=['course', 'semester']),
            models.Index(fields=['teacher']),
            models.Index(fields=['room', 'time_slot']),
        ]
        ordering = ['time_slot__day', 'time_slot__start_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.teacher.email} - {self.time_slot}"


class ScheduleGenerationLog(models.Model):
    """Log for timetable generation attempts."""
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='schedule_generations', limit_choices_to={'role': 'admin'})
    status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('partial', 'Partial'),
    ])
    courses_scheduled = models.IntegerField(default=0)
    conflicts_found = models.IntegerField(default=0)
    conflicts_resolved = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'schedule_generation_logs'
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"Schedule Generation - {self.status} - {self.generated_at}"

