"""
Admin for timetable app.
"""
from django.contrib import admin
from .models import Room, TimeSlot, Timetable, ScheduleGenerationLog


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'building')
    search_fields = ('name', 'building')


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_time', 'end_time')
    list_filter = ('day',)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'room', 'time_slot', 'semester', 'academic_year')
    list_filter = ('semester', 'academic_year', 'time_slot__day', 'course__department')
    search_fields = ('course__code', 'teacher__email', 'room__name')
    readonly_fields = ('created_at',)


@admin.register(ScheduleGenerationLog)
class ScheduleGenerationLogAdmin(admin.ModelAdmin):
    list_display = ('generated_by', 'status', 'courses_scheduled', 'conflicts_found', 'generated_at')
    list_filter = ('status', 'generated_at')
    readonly_fields = ('generated_at',)

