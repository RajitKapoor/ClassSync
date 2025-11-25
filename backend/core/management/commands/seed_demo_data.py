"""
Management command to seed demo data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Department, Course, StudentProfile, TeacherProfile
from assignments.models import Assignment
from exams.models import Exam, Question, Option
from timetable.models import Room, TimeSlot, Timetable
from announcements.models import Announcement
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed demo data for development'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding demo data...')
        
        # Create departments
        dept1, _ = Department.objects.get_or_create(
            code='CS',
            defaults={'name': 'Computer Science', 'description': 'CS Department'}
        )
        dept2, _ = Department.objects.get_or_create(
            code='EE',
            defaults={'name': 'Electrical Engineering', 'description': 'EE Department'}
        )
        dept3, _ = Department.objects.get_or_create(
            code='ME',
            defaults={'name': 'Mechanical Engineering', 'description': 'ME Department'}
        )
        
        # Create admin user
        admin, _ = User.objects.get_or_create(
            email='admin@classsync.com',
            defaults={
                'username': 'admin',
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
            }
        )
        admin.set_password('admin123')
        admin.save()
        
        # Create teachers
        teachers = []
        for i in range(1, 6):
            teacher, _ = User.objects.get_or_create(
                email=f'teacher{i}@classsync.com',
                defaults={
                    'username': f'teacher{i}',
                    'role': 'teacher',
                    'first_name': f'Teacher{i}',
                    'last_name': 'Smith',
                }
            )
            teacher.set_password('teacher123')
            teacher.save()
            
            TeacherProfile.objects.get_or_create(
                user=teacher,
                defaults={
                    'employee_id': f'T{i:03d}',
                    'department': dept1 if i <= 2 else dept2 if i <= 4 else dept3,
                    'specialization': f'Specialization {i}',
                }
            )
            teachers.append(teacher)
        
        # Create students
        students = []
        for i in range(1, 31):
            student, _ = User.objects.get_or_create(
                email=f'student{i}@classsync.com',
                defaults={
                    'username': f'student{i}',
                    'role': 'student',
                    'first_name': f'Student{i}',
                    'last_name': 'Doe',
                }
            )
            student.set_password('student123')
            student.save()
            
            StudentProfile.objects.get_or_create(
                user=student,
                defaults={
                    'student_id': f'S{i:04d}',
                    'department': dept1 if i <= 10 else dept2 if i <= 20 else dept3,
                    'year': (i % 4) + 1,
                    'semester': (i % 2) + 1,
                }
            )
            students.append(student)
        
        # Create courses
        courses = []
        course_data = [
            ('CS101', 'Introduction to Programming', dept1, teachers[0]),
            ('CS201', 'Data Structures', dept1, teachers[1]),
            ('EE101', 'Circuit Analysis', dept2, teachers[2]),
            ('EE201', 'Digital Electronics', dept2, teachers[3]),
        ]
        
        for code, name, dept, teacher in course_data:
            course, _ = Course.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'department': dept,
                    'teacher': teacher,
                    'credits': 3,
                }
            )
            # Enroll students
            course.students.set(students[:20])  # First 20 students
            courses.append(course)
        
        # Create assignments
        for course in courses:
            for i in range(2):
                Assignment.objects.get_or_create(
                    title=f'{course.code} Assignment {i+1}',
                    course=course,
                    defaults={
                        'description': f'Assignment description for {course.code}',
                        'teacher': course.teacher,
                        'deadline': timezone.now() + timedelta(days=7+i*7),
                        'max_marks': 100,
                    }
                )
        
        # Create exams
        for course in courses[:2]:  # First 2 courses
            exam, _ = Exam.objects.get_or_create(
                title=f'{course.code} Midterm Exam',
                course=course,
                defaults={
                    'description': f'Midterm exam for {course.code}',
                    'teacher': course.teacher,
                    'start_time': timezone.now() + timedelta(days=14),
                    'end_time': timezone.now() + timedelta(days=14, hours=2),
                    'duration_minutes': 120,
                    'max_marks': 100,
                    'passing_marks': 40,
                    'is_published': True,
                }
            )
            
            # Create questions
            for q_num in range(1, 6):
                question, _ = Question.objects.get_or_create(
                    exam=exam,
                    order=q_num,
                    defaults={
                        'question_text': f'Question {q_num}: What is the answer?',
                        'question_type': 'mcq',
                        'marks': 20,
                    }
                )
                
                # Create options
                for opt_num in range(1, 5):
                    Option.objects.get_or_create(
                        question=question,
                        order=opt_num,
                        defaults={
                            'option_text': f'Option {opt_num}',
                            'is_correct': opt_num == 1,  # First option is correct
                        }
                    )
        
        # Create rooms
        for i in range(1, 6):
            Room.objects.get_or_create(
                name=f'Room {i}01',
                defaults={
                    'capacity': 50 + i * 10,
                    'building': 'Building A',
                    'facilities': 'projector, whiteboard',
                }
            )
        
        # Create time slots
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        times = [
            ('09:00', '10:30'),
            ('10:45', '12:15'),
            ('13:00', '14:30'),
            ('14:45', '16:15'),
        ]
        
        for day in days:
            for start, end in times:
                TimeSlot.objects.get_or_create(
                    day=day,
                    start_time=start,
                    end_time=end,
                )
        
        # Create announcements
        Announcement.objects.get_or_create(
            title='Welcome to ClassSync',
            defaults={
                'content': 'Welcome to the ClassSync platform. This is a demo announcement.',
                'author': admin,
                'priority': 'high',
                'target_audience': 'all',
                'is_pinned': True,
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded demo data:\n'
                f'- 3 Departments\n'
                f'- 1 Admin user\n'
                f'- 5 Teachers\n'
                f'- 30 Students\n'
                f'- 4 Courses\n'
                f'- 8 Assignments\n'
                f'- 2 Exams with questions\n'
                f'- 5 Rooms\n'
                f'- Time slots\n'
                f'- 1 Announcement\n'
            )
        )

