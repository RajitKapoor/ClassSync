"""
Management command to send deadline reminders for assignments.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from assignments.models import Assignment, DeadlineNotification
from announcements.models import Notification
from accounts.models import User


class Command(BaseCommand):
    help = 'Send deadline reminders for upcoming assignments'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Hours before deadline to send reminder (default: 24)',
        )
    
    def handle(self, *args, **options):
        hours = options['hours']
        reminder_time = timezone.now() + timedelta(hours=hours)
        
        # Find assignments with deadlines in the reminder window
        assignments = Assignment.objects.filter(
            deadline__gte=timezone.now(),
            deadline__lte=reminder_time
        )
        
        reminder_type = '24h' if hours == 24 else '1h' if hours == 1 else 'overdue'
        
        reminders_sent = 0
        
        for assignment in assignments:
            # Get all students enrolled in the course
            students = assignment.course.students.filter(role='student')
            
            for student in students:
                # Check if already submitted
                if assignment.submissions.filter(student=student).exists():
                    continue
                
                # Check if reminder already sent
                if DeadlineNotification.objects.filter(
                    assignment=assignment,
                    student=student,
                    reminder_type=reminder_type
                ).exists():
                    continue
                
                # Create notification
                Notification.objects.create(
                    user=student,
                    title=f'Assignment Deadline Reminder',
                    message=f'Assignment "{assignment.title}" is due in {hours} hours. Please submit before {assignment.deadline}.',
                    link=f'/assignments/{assignment.id}'
                )
                
                # Log reminder
                DeadlineNotification.objects.create(
                    assignment=assignment,
                    student=student,
                    reminder_type=reminder_type
                )
                
                reminders_sent += 1
                
                # In development, print to console (email backend will also print)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Reminder sent to {student.email} for assignment "{assignment.title}"'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully sent {reminders_sent} deadline reminders.'
            )
        )

