# Developer Guide

## Table of Contents
1. [Database Schema](#database-schema)
2. [API Endpoints](#api-endpoints)
3. [Adding New Features](#adding-new-features)
4. [Running Migrations](#running-migrations)
5. [Background Tasks](#background-tasks)
6. [Testing](#testing)

## Database Schema

### Core Models

#### User (accounts.User)
- Custom user model with email-based authentication
- Roles: student, teacher, admin
- Extended profiles: StudentProfile, TeacherProfile

#### Course (accounts.Course)
- Belongs to Department
- Has many Students (M2M)
- Has one Teacher

#### Assignment (assignments.Assignment)
- Belongs to Course and Teacher
- Has many Submissions
- Deadline tracking

#### Submission (assignments.Submission)
- Belongs to Assignment and Student
- File uploads supported
- Grading fields

#### LeaveRequest (leave.LeaveRequest)
- Belongs to Student
- Status: pending, approved, rejected
- Analytics tracking

#### Timetable (timetable.Timetable)
- Links Course, Teacher, Room, TimeSlot
- Conflict detection in generation

#### Exam (exams.Exam)
- Belongs to Course and Teacher
- Has many Questions
- Auto-grading support

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/forgot-password/` - Request password reset
- `POST /api/auth/reset-password/<uid>/<token>/` - Reset password
- `GET /api/auth/me/` - Get current user

### Assignments
- `GET /api/assignments/` - List assignments
- `POST /api/assignments/` - Create assignment (teacher)
- `GET /api/assignments/{id}/` - Get assignment details
- `POST /api/assignments/{id}/submissions/` - Submit assignment
- `POST /api/assignments/{id}/submissions/{id}/grade/` - Grade submission

### Announcements
- `GET /api/announcements/` - List announcements
- `POST /api/announcements/` - Create announcement
- `GET /api/announcements/notifications/` - Get notifications

### Leave
- `GET /api/leave/` - List leave requests
- `POST /api/leave/` - Create leave request
- `POST /api/leave/{id}/approve/` - Approve leave
- `POST /api/leave/{id}/reject/` - Reject leave
- `GET /api/leave/analytics/` - Get analytics

### Timetable
- `GET /api/timetable/` - Get timetable
- `POST /api/timetable/generate/` - Generate timetable (admin)

### Exams
- `GET /api/exams/` - List exams
- `POST /api/exams/` - Create exam (teacher)
- `POST /api/exams/{id}/submit/` - Submit exam
- `GET /api/exams/{id}/results/` - Get results

### Dashboard
- `GET /api/dashboard/student/` - Student dashboard
- `GET /api/dashboard/teacher/` - Teacher dashboard
- `GET /api/dashboard/admin/` - Admin dashboard

## Adding New Features

### 1. Create Model
```python
# In your app/models.py
class MyModel(models.Model):
    field = models.CharField(max_length=100)
    # ... other fields
```

### 2. Create Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Serializer
```python
# In your app/serializers.py
class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

### 4. Create ViewSet
```python
# In your app/views.py
class MyModelViewSet(viewsets.ModelViewSet):
    serializer_class = MyModelSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MyModel.objects.all()
```

### 5. Add URL
```python
# In your app/urls.py
router.register(r'my-models', MyModelViewSet, basename='mymodel')
```

### 6. Register in Admin
```python
# In your app/admin.py
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('field',)
```

## Running Migrations

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Rollback (if needed)
```bash
python manage.py migrate app_name previous_migration_number
```

## Background Tasks

### Deadline Reminders

The system includes a management command to send deadline reminders:

```bash
python manage.py send_deadline_reminders --hours 24
```

### Setting Up Cron Jobs

For production, set up a cron job to run reminders:

```bash
# Edit crontab
crontab -e

# Add line to run every day at 9 AM
0 9 * * * cd /path/to/project && python manage.py send_deadline_reminders --hours 24
```

### Using GitHub Actions (Free Alternative)

Create `.github/workflows/reminders.yml`:

```yaml
name: Send Reminders
on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM
jobs:
  send:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: python manage.py send_deadline_reminders --hours 24
```

## Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run specific app
pytest accounts/

# With coverage
pytest --cov=accounts --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Writing Tests

#### Backend Example
```python
# tests/test_models.py
def test_assignment_creation():
    assignment = Assignment.objects.create(
        title="Test",
        course=course,
        teacher=teacher,
        deadline=timezone.now() + timedelta(days=7)
    )
    assert assignment.title == "Test"
```

#### Frontend Example
```javascript
// Assignment.test.jsx
import { render, screen } from '@testing-library/react';
import Assignments from './Assignments';

test('renders assignments', () => {
  render(<Assignments />);
  expect(screen.getByText('Assignments')).toBeInTheDocument();
});
```

## Code Style

### Python
- Use `black` for formatting
- Use `isort` for imports
- Follow PEP 8

### JavaScript
- Use ESLint
- Follow React best practices
- Use functional components with hooks

## Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Database Configuration

### SQLite (Default - Development)
No configuration needed. Works out of the box.

### PostgreSQL (Production)
Uncomment in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'classsync',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Troubleshooting

### Common Issues

1. **Migration conflicts**: Delete migration files and recreate
2. **CORS errors**: Check `CORS_ALLOWED_ORIGINS` in settings
3. **Token authentication**: Ensure token is in `Authorization: Token <token>` header

## Performance Tips

1. Use `select_related()` for foreign keys
2. Use `prefetch_related()` for M2M and reverse FK
3. Add database indexes for frequently queried fields
4. Use pagination for large datasets

## Security Best Practices

1. Never commit `.env` files
2. Use strong passwords
3. Enable CSRF protection
4. Use HTTPS in production
5. Validate all user inputs
6. Use parameterized queries (Django ORM does this)

