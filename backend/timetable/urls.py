"""
URLs for timetable app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, TimeSlotViewSet, TimetableViewSet, ScheduleGenerationLogViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'time-slots', TimeSlotViewSet, basename='timeslot')
router.register(r'', TimetableViewSet, basename='timetable')
router.register(r'generation-logs', ScheduleGenerationLogViewSet, basename='generation-log')

urlpatterns = [
    path('', include(router.urls)),
]

