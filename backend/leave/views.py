"""
Views for leave app.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from .models import LeaveRequest, LeaveAnalytics
from .serializers import LeaveRequestSerializer, LeaveAnalyticsSerializer


class IsAdminOrTeacher(permissions.BasePermission):
    """Permission for admin or teacher."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_teacher)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for leave requests."""
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return LeaveRequest.objects.filter(student=user)
        elif user.is_teacher or user.is_admin:
            # Teachers/admins can see all leave requests
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a leave request."""
        if not (request.user.is_admin or request.user.is_teacher):
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        leave_request = self.get_object()
        leave_request.status = 'approved'
        leave_request.approved_by = request.user
        leave_request.save()
        
        # Update analytics
        self._update_analytics(leave_request)
        
        serializer = self.get_serializer(leave_request)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a leave request."""
        if not (request.user.is_admin or request.user.is_teacher):
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        leave_request = self.get_object()
        leave_request.status = 'rejected'
        leave_request.approved_by = request.user
        leave_request.rejection_reason = request.data.get('rejection_reason', '')
        leave_request.save()
        
        # Update analytics
        self._update_analytics(leave_request)
        
        serializer = self.get_serializer(leave_request)
        return Response(serializer.data)
    
    def _update_analytics(self, leave_request):
        """Update leave analytics for the student."""
        year = leave_request.start_date.year
        analytics, created = LeaveAnalytics.objects.get_or_create(
            student=leave_request.student,
            year=year,
            defaults={
                'total_leaves': 0,
                'approved_leaves': 0,
                'rejected_leaves': 0,
                'pending_leaves': 0,
                'total_days': 0,
            }
        )
        
        # Recalculate all stats
        leaves = LeaveRequest.objects.filter(student=leave_request.student, start_date__year=year)
        analytics.total_leaves = leaves.count()
        analytics.approved_leaves = leaves.filter(status='approved').count()
        analytics.rejected_leaves = leaves.filter(status='rejected').count()
        analytics.pending_leaves = leaves.filter(status='pending').count()
        analytics.total_days = sum(leave.duration_days for leave in leaves.filter(status='approved'))
        analytics.save()
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get leave analytics."""
        if not (request.user.is_admin or request.user.is_teacher):
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        year = request.query_params.get('year', None)
        queryset = LeaveAnalytics.objects.all()
        
        if year:
            queryset = queryset.filter(year=year)
        
        serializer = LeaveAnalyticsSerializer(queryset, many=True)
        return Response(serializer.data)

