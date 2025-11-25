"""
Leave management models.
"""
from django.db import models
from accounts.models import User


class LeaveRequest(models.Model):
    """Leave request model."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    LEAVE_TYPE_CHOICES = [
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('emergency', 'Emergency Leave'),
        ('other', 'Other'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests', limit_choices_to={'role': 'student'})
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, default='casual')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves', limit_choices_to={'role__in': ['admin', 'teacher']})
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leave_requests'
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date', 'end_date']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.email} - {self.start_date} to {self.end_date} ({self.status})"
    
    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1


class LeaveAnalytics(models.Model):
    """Leave analytics model (can be computed or stored)."""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_analytics', limit_choices_to={'role': 'student'})
    year = models.IntegerField()
    total_leaves = models.IntegerField(default=0)
    approved_leaves = models.IntegerField(default=0)
    rejected_leaves = models.IntegerField(default=0)
    pending_leaves = models.IntegerField(default=0)
    total_days = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'leave_analytics'
        unique_together = ['student', 'year']
        indexes = [
            models.Index(fields=['student', 'year']),
        ]
    
    def __str__(self):
        return f"{self.student.email} - {self.year}"

