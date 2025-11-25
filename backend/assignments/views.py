"""
Views for assignments app.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer
from accounts.models import Course


class IsTeacherOrReadOnly(permissions.BasePermission):
    """Permission to allow only teachers to create/edit assignments."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_teacher


class AssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for assignments."""
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacherOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return Assignment.objects.filter(teacher=user)
        elif user.is_student:
            # Get assignments for courses the student is enrolled in
            return Assignment.objects.filter(course__students=user).distinct()
        elif user.is_admin:
            return Assignment.objects.all()
        return Assignment.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get all submissions for an assignment."""
        assignment = self.get_object()
        if not (request.user.is_teacher or request.user.is_admin):
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        submissions = assignment.submissions.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)


class SubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for submissions."""
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_teacher or user.is_admin:
            return Submission.objects.all()
        elif user.is_student:
            return Submission.objects.filter(student=user)
        return Submission.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        """Grade a submission (teacher only)."""
        if not (request.user.is_teacher or request.user.is_admin):
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        submission = self.get_object()
        marks_obtained = request.data.get('marks_obtained')
        feedback = request.data.get('feedback', '')
        
        if marks_obtained is None:
            return Response({'error': 'marks_obtained is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        submission.marks_obtained = marks_obtained
        submission.feedback = feedback
        submission.is_graded = True
        submission.save()
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)

