# ClassSync - College ERP System

A fully functional College ERP (Enterprise Resource Planning) system built with Django and React, using only free and open-source technologies.

## 🎯 Project Overview

ClassSync is a comprehensive college management system that provides role-based dashboards, assignment management, announcements, leave management, timetable generation, online exams, and student progress tracking - all built with zero monetary cost for the tech stack.

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│   React Frontend │ ◄─────► │  Django Backend │
│   (Vite + Tailwind)       │  (DRF + AllAuth) │
└─────────────────┘         └─────────────────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │   SQLite /      │
                            │   PostgreSQL    │
                            └─────────────────┘
```

## ✨ Features

### Core Features (MVP)
1. **Role-based Dashboards**
   - Student Dashboard: Upcoming classes, attendance, pending assignments
   - Teacher Dashboard: Today's classes, pending grading, quick actions
   - Admin Dashboard: System stats, analytics, health checks

2. **Assignment Management**
   - Upload assignments with deadlines
   - Student submissions with file uploads
   - Automatic deadline reminders
   - Grading and feedback system

3. **Announcements & Notifications**
   - Priority-based announcements
   - Role-specific targeting
   - Real-time notification panel

4. **Leave Management**
   - Apply for leave (students)
   - Approve/reject leave (teachers/admins)
   - Leave analytics and tracking

5. **Student Progress Analysis**
   - Attendance trends (charts)
   - Marks graphs
   - Performance predictions

6. **Automated Timetable Generator**
   - Conflict detection and resolution
   - Admin-triggered regeneration
   - Room and teacher scheduling

7. **Online Exams/Quizzes**
   - MCQ and short answer questions
   - Auto-grading for MCQs
   - Exam results and analytics

8. **Authentication**
   - Email-based login
   - Password reset flow
   - Role-based access control

## 🛠️ Tech Stack

### Backend
- **Django 5.0** - Web framework
- **Django REST Framework** - API development
- **Django AllAuth** - Authentication
- **SQLite** - Development database (default)
- **PostgreSQL** - Production database (optional, free tier)

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client

### Development Tools
- **pytest** - Testing
- **black, isort, flake8** - Code quality
- **GitHub Actions** - CI/CD

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- pip and npm

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/RajitKapoor/ClassSync.git
   cd ClassSync
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r ../requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Seed demo data (optional)**
   ```bash
   python manage.py seed_demo_data
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔍 Code Quality

### Linting & Formatting
```bash
# Backend
black backend/
isort backend/
flake8 backend/

# Frontend
cd frontend
npm run lint
```

## 📚 API Documentation

Once the backend is running, access the API documentation at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔐 Default Credentials (Demo Data)

After running `seed_demo_data`:
- **Admin**: admin@classsync.com / admin123
- **Teacher**: teacher1@classsync.com / teacher123
- **Student**: student1@classsync.com / student123

## 📁 Project Structure

```
ClassSync/
├── backend/
│   ├── accounts/          # User management
│   ├── assignments/       # Assignment & submission
│   ├── announcements/      # Announcements & notifications
│   ├── leave/             # Leave management
│   ├── timetable/         # Timetable generation
│   ├── exams/             # Online exams
│   ├── dashboard/         # Dashboard APIs
│   ├── core/              # Management commands
│   └── config/            # Django settings
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── context/       # React context
│   └── public/
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
└── README.md
```

## 🔄 Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - Feature branches
- `fix/*` - Bug fix branches

## 🚀 Deployment

### Backend (Free Options)
- **Railway** (free tier)
- **Render** (free tier)
- **Heroku** (if free tier available)

### Frontend (Free Options)
- **Vercel** (free tier)
- **Netlify** (free tier)
- **GitHub Pages**

See `/docs/dev_guide.md` for detailed deployment instructions.

## 📝 Management Commands

### Send Deadline Reminders
```bash
python manage.py send_deadline_reminders --hours 24
```

### Seed Demo Data
```bash
python manage.py seed_demo_data
```

## 🤝 Contributing

1. Create a feature branch from `develop`
2. Make your changes
3. Write tests
4. Submit a PR to `develop`

See `/docs/dev_guide.md` for detailed contribution guidelines.

## 📄 License

This project is open source and available under the MIT License.

## 🐛 Issues & Support

For issues, feature requests, or questions, please open an issue on GitHub.

## 📖 Additional Documentation

- [Developer Guide](/docs/dev_guide.md)
- [User Guide](/docs/user_guide.md)

---

Built with ❤️ using free and open-source technologies.
