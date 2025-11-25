"""
Views for timetable app.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Room, TimeSlot, Timetable, ScheduleGenerationLog
from .serializers import RoomSerializer, TimeSlotSerializer, TimetableSerializer, ScheduleGenerationLogSerializer
from accounts.models import Course
from .utils import generate_timetable


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet for rooms."""
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Room.objects.all()


class TimeSlotViewSet(viewsets.ModelViewSet):
    """ViewSet for time slots."""
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TimeSlot.objects.all()


class TimetableViewSet(viewsets.ModelViewSet):
    """ViewSet for timetable."""
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        semester = self.request.query_params.get('semester')
        academic_year = self.request.query_params.get('academic_year')
        
        queryset = Timetable.objects.all()
        
        if user.is_student:
            # Show timetable for courses student is enrolled in
            queryset = queryset.filter(course__students=user)
        elif user.is_teacher:
            # Show timetable for courses teacher teaches
            queryset = queryset.filter(teacher=user)
        
        if semester:
            queryset = queryset.filter(semester=semester)
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        return queryset.order_by('time_slot__day', 'time_slot__start_time')
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def generate(self, request):
        """Generate timetable automatically (admin only)."""
        semester = request.data.get('semester', 1)
        academic_year = request.data.get('academic_year', '2024-2025')
        
        try:
            result = generate_timetable(semester, academic_year, request.user)
            
            log = ScheduleGenerationLog.objects.create(
                generated_by=request.user,
                status=result['status'],
                courses_scheduled=result['courses_scheduled'],
                conflicts_found=result['conflicts_found'],
                conflicts_resolved=result['conflicts_resolved'],
                error_message=result.get('error_message', '')
            )
            
            serializer = ScheduleGenerationLogSerializer(log)
            return Response({
                'message': 'Timetable generation completed.',
                'log': serializer.data,
                'timetable': result.get('timetable', [])
            }, status=status.HTTP_200_OK)
        except Exception as e:
            log = ScheduleGenerationLog.objects.create(
                generated_by=request.user,
                status='failed',
                courses_scheduled=0,
                conflicts_found=0,
                conflicts_resolved=0,
                error_message=str(e)
            )
            return Response({
                'error': 'Timetable generation failed.',
                'log': ScheduleGenerationLogSerializer(log).data
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ScheduleGenerationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for schedule generation logs."""
    serializer_class = ScheduleGenerationLogSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = ScheduleGenerationLog.objects.all()

