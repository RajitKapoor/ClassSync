"""
Tests for assignments app.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import Department, Course
from .models import Assignment, Submission

User = get_user_model()


class AssignmentModelTest(TestCase):
    """Test Assignment model."""
    
    def setUp(self):
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS'
        )
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            username='teacher',
            password='testpass123',
            role='teacher'
        )
        self.course = Course.objects.create(
            name='Test Course',
            code='CS101',
            department=self.department,
            teacher=self.teacher
        )
    
    def test_assignment_creation(self):
        assignment = Assignment.objects.create(
            title='Test Assignment',
            description='Test description',
            course=self.course,
            teacher=self.teacher,
            deadline=timezone.now() + timedelta(days=7),
            max_marks=100
        )
        self.assertEqual(assignment.title, 'Test Assignment')
        self.assertFalse(assignment.is_overdue)
        self.assertEqual(assignment.submission_count, 0)


class AssignmentAPITest(TestCase):
    """Test Assignment API."""
    
    def setUp(self):
        self.client = APIClient()
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS'
        )
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            username='teacher',
            password='testpass123',
            role='teacher'
        )
        self.student = User.objects.create_user(
            email='student@example.com',
            username='student',
            password='testpass123',
            role='student'
        )
        self.course = Course.objects.create(
            name='Test Course',
            code='CS101',
            department=self.department,
            teacher=self.teacher
        )
        self.course.students.add(self.student)
    
    def test_create_assignment(self):
        self.client.force_authenticate(user=self.teacher)
        data = {
            'title': 'New Assignment',
            'description': 'Description',
            'course_id': self.course.id,
            'deadline': (timezone.now() + timedelta(days=7)).isoformat(),
            'max_marks': 100
        }
        response = self.client.post('/api/assignments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_assignments(self):
        Assignment.objects.create(
            title='Test Assignment',
            description='Test',
            course=self.course,
            teacher=self.teacher,
            deadline=timezone.now() + timedelta(days=7)
        )
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/assignments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

