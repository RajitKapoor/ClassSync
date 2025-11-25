# User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Student Guide](#student-guide)
3. [Teacher Guide](#teacher-guide)
4. [Admin Guide](#admin-guide)

## Getting Started

### Registration
1. Navigate to the registration page
2. Fill in your details:
   - Email (required)
   - Username (required)
   - First Name, Last Name
   - Role (Student or Teacher)
   - Password (minimum 8 characters)
3. Click "Register"
4. You'll be automatically logged in

### Login
1. Go to the login page
2. Enter your email and password
3. Click "Sign in"
4. You'll be redirected to your role-specific dashboard

### Forgot Password
1. Click "Forgot your password?" on the login page
2. Enter your email address
3. Check your email (or console in dev mode) for reset link
4. Click the link and enter your new password

## Student Guide

### Dashboard
Your dashboard shows:
- **Upcoming Classes**: Next 7 days of classes
- **Attendance**: Current attendance percentage
- **Pending Assignments**: Assignments due soon
- **Recent Announcements**: Latest updates
- **Unread Notifications**: Count of unread notifications
- **Upcoming Exams**: Exams scheduled soon

### Assignments
1. View all assignments for your enrolled courses
2. Click on an assignment to view details
3. Submit your work:
   - Enter text content
   - Upload files (if required)
   - Submit before deadline
4. View feedback and grades after submission is graded

### Announcements
- View all announcements relevant to you
- Pinned announcements appear at the top
- Filter by priority (urgent, high, medium, low)

### Leave Management
1. Click "Apply for Leave"
2. Fill in the form:
   - Leave type (sick, casual, emergency, other)
   - Start date and end date
   - Reason
3. Submit your request
4. Track status: pending, approved, or rejected
5. View rejection reason if rejected

### Timetable
- View your weekly class schedule
- Organized by day of the week
- Shows course, time, room, and teacher

### Exams
1. View all published exams
2. Click "Take Exam" when exam is active
3. Answer questions:
   - MCQs: Select correct options
   - Short answers: Type your answer
4. Submit before time expires
5. View results after grading

## Teacher Guide

### Dashboard
Your dashboard shows:
- **Today's Classes**: Classes scheduled for today
- **Pending Grading**: Submissions awaiting grading
- **Recent Assignments**: Assignments you created
- **Statistics**: Courses taught, total students, pending grading count

### Creating Assignments
1. Go to Assignments page
2. Click "Create Assignment"
3. Fill in:
   - Title
   - Description
   - Course ID
   - Deadline (date and time)
   - Maximum marks
4. Optionally upload a file
5. Click "Create"

### Grading Submissions
1. Go to Assignments page
2. View submissions for your assignments
3. Click on a submission
4. Enter marks and feedback
5. Click "Grade" to save

### Creating Exams
1. Go to Exams page
2. Create exam with:
   - Title and description
   - Course
   - Start and end time
   - Duration
   - Maximum and passing marks
3. Add questions:
   - MCQ: Add question text and options (mark correct ones)
   - Short answer: Add question text
4. Publish exam when ready
5. View results after students submit

### Leave Approval
1. Go to Leave Management page
2. View pending leave requests
3. Click "Approve" or "Reject"
4. If rejecting, provide a reason

## Admin Guide

### Dashboard
Your dashboard shows:
- **System Statistics**: Total students, teachers, courses, assignments, exams
- **Recent Leave Requests**: Pending approvals
- **Attendance Analytics**: System-wide attendance trends
- **Database Health**: System status

### Timetable Generation
1. Go to Timetable page
2. Click "Generate Timetable"
3. System will:
   - Check for conflicts (teacher, room, time)
   - Resolve conflicts automatically
   - Generate schedule
4. View generation log for details

### User Management
1. Access Django admin panel at `/admin`
2. Manage users, courses, departments
3. Create student/teacher profiles
4. Assign courses to teachers and students

### System Configuration
- Configure departments
- Set up rooms and time slots
- Manage system-wide settings

## Tips & Best Practices

### For Students
- Check dashboard daily for updates
- Submit assignments before deadline
- Check announcements regularly
- Keep track of exam schedules
- Apply for leave in advance

### For Teachers
- Grade submissions promptly
- Create assignments with clear instructions
- Set realistic deadlines
- Provide constructive feedback
- Publish exams well in advance

### For Admins
- Monitor system health regularly
- Review leave requests promptly
- Generate timetable at start of semester
- Keep user data updated
- Review analytics for insights

## Troubleshooting

### Can't log in?
- Check email and password
- Use "Forgot Password" if needed
- Contact admin if account is locked

### Assignment not showing?
- Ensure you're enrolled in the course
- Check if assignment is published
- Refresh the page

### Exam not accessible?
- Check exam start time
- Ensure exam is published
- Verify you're enrolled in the course

### Leave request not approved?
- Check with your teacher/admin
- Review rejection reason if provided
- Reapply if needed

## Keyboard Shortcuts

- `Tab` - Navigate between form fields
- `Enter` - Submit forms
- `Esc` - Close modals/dialogs

## Accessibility

- All forms support keyboard navigation
- Screen reader compatible
- High contrast mode available
- Dark mode toggle in navigation

## Support

For technical issues or questions:
1. Check this user guide
2. Review FAQ section
3. Contact your system administrator
4. Open an issue on GitHub (for developers)

