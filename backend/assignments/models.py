"""
Assignment and submission models.
"""
from django.db import models
from django.utils import timezone
from accounts.models import User, Course


class Assignment(models.Model):
    """Assignment model."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_assignments', limit_choices_to={'role': 'teacher'})
    deadline = models.DateTimeField()
    max_marks = models.IntegerField(default=100)
    file_attachment = models.FileField(upload_to='assignments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assignments'
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['deadline']),
            models.Index(fields=['teacher']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.course.code}"
    
    @property
    def is_overdue(self):
        return timezone.now() > self.deadline
    
    @property
    def submission_count(self):
        return self.submissions.count()


class Submission(models.Model):
    """Student submission model."""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions', limit_choices_to={'role': 'student'})
    content = models.TextField(blank=True)
    file_attachment = models.FileField(upload_to='submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    marks_obtained = models.IntegerField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    is_graded = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'submissions'
        unique_together = ['assignment', 'student']
        indexes = [
            models.Index(fields=['assignment', 'student']),
            models.Index(fields=['student']),
            models.Index(fields=['submitted_at']),
        ]
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.email} - {self.assignment.title}"
    
    @property
    def is_late(self):
        return self.submitted_at > self.assignment.deadline


class DeadlineNotification(models.Model):
    """Model to track deadline reminders sent."""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='notifications')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deadline_notifications', limit_choices_to={'role': 'student'})
    reminder_sent_at = models.DateTimeField(auto_now_add=True)
    reminder_type = models.CharField(max_length=20, choices=[
        ('24h', '24 Hours Before'),
        ('1h', '1 Hour Before'),
        ('overdue', 'Overdue'),
    ])
    
    class Meta:
        db_table = 'deadline_notifications'
        unique_together = ['assignment', 'student', 'reminder_type']
        indexes = [
            models.Index(fields=['assignment', 'student']),
        ]

