"""
Dashboard views for role-based dashboards.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from django.db.models import Count, Q, Avg, Sum
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, Course
from assignments.models import Assignment, Submission
from announcements.models import Announcement, Notification
from leave.models import LeaveRequest
from timetable.models import Timetable
from exams.models import Exam, AutoGradingResult


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def student_dashboard(request):
    """Student dashboard data."""
    if not request.user.is_student:
        return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    student = request.user
    
    # Upcoming classes (next 7 days)
    today = timezone.now().date()
    week_from_now = today + timedelta(days=7)
    upcoming_classes = Timetable.objects.filter(
        course__students=student
    ).select_related('course', 'teacher', 'room', 'time_slot').order_by('time_slot__day', 'time_slot__start_time')[:10]
    
    # Attendance (placeholder - would need attendance model)
    attendance_percent = 85.5  # Mock data
    
    # Pending assignments
    pending_assignments = Assignment.objects.filter(
        course__students=student,
        deadline__gte=timezone.now()
    ).exclude(
        submissions__student=student
    ).select_related('course', 'teacher').order_by('deadline')[:5]
    
    # Recent announcements
    recent_announcements = Announcement.objects.filter(
        Q(target_audience='all') | Q(target_audience='students') | Q(course__students=student)
    ).distinct().order_by('-created_at')[:5]
    
    # Unread notifications
    unread_notifications = Notification.objects.filter(user=student, is_read=False).count()
    
    # Upcoming exams
    upcoming_exams = Exam.objects.filter(
        course__students=student,
        is_published=True,
        start_time__gte=timezone.now()
    ).select_related('course', 'teacher').order_by('start_time')[:5]
    
    return Response({
        'upcoming_classes': [{
            'id': cls.id,
            'course': cls.course.code,
            'course_name': cls.course.name,
            'teacher': f"{cls.teacher.first_name} {cls.teacher.last_name}",
            'room': cls.room.name if cls.room else None,
            'day': cls.time_slot.day,
            'time': f"{cls.time_slot.start_time} - {cls.time_slot.end_time}",
        } for cls in upcoming_classes],
        'attendance': {
            'percent': attendance_percent,
        },
        'pending_assignments': [{
            'id': ass.id,
            'title': ass.title,
            'course': ass.course.code,
            'deadline': ass.deadline,
            'is_overdue': ass.is_overdue,
        } for ass in pending_assignments],
        'recent_announcements': [{
            'id': ann.id,
            'title': ann.title,
            'priority': ann.priority,
            'created_at': ann.created_at,
        } for ann in recent_announcements],
        'unread_notifications': unread_notifications,
        'upcoming_exams': [{
            'id': exam.id,
            'title': exam.title,
            'course': exam.course.code,
            'start_time': exam.start_time,
            'duration_minutes': exam.duration_minutes,
        } for exam in upcoming_exams],
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def teacher_dashboard(request):
    """Teacher dashboard data."""
    if not request.user.is_teacher:
        return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    teacher = request.user
    
    # Today's classes
    today = timezone.now().date()
    today_classes = Timetable.objects.filter(
        teacher=teacher,
        time_slot__day=today.strftime('%A').lower()
    ).select_related('course', 'room', 'time_slot').order_by('time_slot__start_time')
    
    # Pending grading
    pending_grading = Submission.objects.filter(
        assignment__teacher=teacher,
        is_graded=False
    ).select_related('assignment', 'student').order_by('submitted_at')[:10]
    
    # Recent assignments created
    recent_assignments = Assignment.objects.filter(teacher=teacher).order_by('-created_at')[:5]
    
    # Courses taught
    courses_taught = Course.objects.filter(teacher=teacher).count()
    
    # Total students
    total_students = User.objects.filter(
        enrolled_courses__teacher=teacher
    ).distinct().count()
    
    return Response({
        'today_classes': [{
            'id': cls.id,
            'course': cls.course.code,
            'course_name': cls.course.name,
            'room': cls.room.name if cls.room else None,
            'time': f"{cls.time_slot.start_time} - {cls.time_slot.end_time}",
        } for cls in today_classes],
        'pending_grading': [{
            'id': sub.id,
            'assignment': sub.assignment.title,
            'student': sub.student.email,
            'submitted_at': sub.submitted_at,
            'is_late': sub.is_late,
        } for sub in pending_grading],
        'recent_assignments': [{
            'id': ass.id,
            'title': ass.title,
            'course': ass.course.code,
            'deadline': ass.deadline,
            'submission_count': ass.submission_count,
        } for ass in recent_assignments],
        'stats': {
            'courses_taught': courses_taught,
            'total_students': total_students,
            'pending_grading_count': pending_grading.count(),
        },
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def admin_dashboard(request):
    """Admin dashboard data."""
    if not request.user.is_admin:
        return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)
    
    # Total counts
    total_students = User.objects.filter(role='student').count()
    total_teachers = User.objects.filter(role='teacher').count()
    total_courses = Course.objects.count()
    total_assignments = Assignment.objects.count()
    total_exams = Exam.objects.count()
    
    # Recent leave requests
    recent_leaves = LeaveRequest.objects.filter(status='pending').order_by('-created_at')[:10]
    
    # Attendance analytics (mock)
    attendance_analytics = {
        'average_attendance': 82.5,
        'trend': 'increasing',
    }
    
    # Database health (simple check)
    db_health = {
        'status': 'healthy',
        'total_users': User.objects.count(),
        'total_courses': total_courses,
    }
    
    return Response({
        'stats': {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'total_assignments': total_assignments,
            'total_exams': total_exams,
        },
        'recent_leaves': [{
            'id': leave.id,
            'student': leave.student.email,
            'leave_type': leave.leave_type,
            'start_date': leave.start_date,
            'end_date': leave.end_date,
            'status': leave.status,
        } for leave in recent_leaves],
        'attendance_analytics': attendance_analytics,
        'db_health': db_health,
    })

