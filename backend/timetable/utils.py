"""
Timetable generation utilities.
"""
from django.db.models import Q
from .models import Timetable, Room, TimeSlot
from accounts.models import Course


def generate_timetable(semester, academic_year, generated_by):
    """
    Generate timetable using a simple greedy algorithm.
    Returns a dict with status, courses_scheduled, conflicts info.
    """
    courses = Course.objects.filter(students__isnull=False).distinct()
    rooms = Room.objects.all()
    time_slots = TimeSlot.objects.all().order_by('day', 'start_time')
    
    scheduled = []
    conflicts_found = 0
    conflicts_resolved = 0
    
    # Clear existing timetable for this semester/year
    Timetable.objects.filter(semester=semester, academic_year=academic_year).delete()
    
    for course in courses:
        if not course.teacher:
            continue
        
        scheduled_this_course = False
        
        for time_slot in time_slots:
            # Check for teacher conflict
            teacher_busy = Timetable.objects.filter(
                teacher=course.teacher,
                time_slot=time_slot,
                semester=semester,
                academic_year=academic_year
            ).exists()
            
            if teacher_busy:
                conflicts_found += 1
                continue
            
            # Check for room availability
            available_room = None
            for room in rooms:
                room_busy = Timetable.objects.filter(
                    room=room,
                    time_slot=time_slot,
                    semester=semester,
                    academic_year=academic_year
                ).exists()
                
                if not room_busy and room.capacity >= course.students.count():
                    available_room = room
                    break
            
            if available_room:
                timetable_entry = Timetable.objects.create(
                    course=course,
                    teacher=course.teacher,
                    room=available_room,
                    time_slot=time_slot,
                    semester=semester,
                    academic_year=academic_year
                )
                scheduled.append(timetable_entry)
                scheduled_this_course = True
                conflicts_resolved += 1
                break
        
        if not scheduled_this_course:
            conflicts_found += 1
    
    status = 'success' if len(scheduled) == courses.count() else 'partial'
    if len(scheduled) == 0:
        status = 'failed'
    
    return {
        'status': status,
        'courses_scheduled': len(scheduled),
        'conflicts_found': conflicts_found,
        'conflicts_resolved': conflicts_resolved,
        'timetable': [{
            'id': t.id,
            'course': t.course.code,
            'teacher': t.teacher.email,
            'room': t.room.name if t.room else None,
            'time_slot': f"{t.time_slot.day} {t.time_slot.start_time}-{t.time_slot.end_time}"
        } for t in scheduled]
    }

