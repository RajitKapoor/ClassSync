import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import ForgotPassword from './pages/ForgotPassword';
import StudentDashboard from './pages/StudentDashboard';
import TeacherDashboard from './pages/TeacherDashboard';
import AdminDashboard from './pages/AdminDashboard';
import Assignments from './pages/Assignments';
import Announcements from './pages/Announcements';
import LeaveManagement from './pages/LeaveManagement';
import Timetable from './pages/Timetable';
import Exams from './pages/Exams';
import Layout from './components/Layout';

const PrivateRoute = ({ children, allowedRoles = [] }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" />;
  }

  if (allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
    return <Navigate to={`/${user.role}/dashboard`} />;
  }

  return children;
};

function AppRoutes() {
  const { user } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={!user ? <Login /> : <Navigate to={`/${user.role}/dashboard`} />} />
      <Route path="/register" element={!user ? <Register /> : <Navigate to={`/${user.role}/dashboard`} />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      
      <Route
        path="/student/dashboard"
        element={
          <PrivateRoute allowedRoles={['student']}>
            <Layout>
              <StudentDashboard />
            </Layout>
          </PrivateRoute>
        }
      />
      <Route
        path="/teacher/dashboard"
        element={
          <PrivateRoute allowedRoles={['teacher']}>
            <Layout>
              <TeacherDashboard />
            </Layout>
          </PrivateRoute>
        }
      />
      <Route
        path="/admin/dashboard"
        element={
          <PrivateRoute allowedRoles={['admin']}>
            <Layout>
              <AdminDashboard />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route
        path="/assignments"
        element={
          <PrivateRoute>
            <Layout>
              <Assignments />
            </Layout>
          </PrivateRoute>
        }
      />
      <Route
        path="/announcements"
        element={
          <PrivateRoute>
            <Layout>
              <Announcements />
            </Layout>
          </PrivateRoute>
        }
      />
      <Route
        path="/leave"
        element={
          <PrivateRoute>
            <Layout>
              <LeaveManagement />
            </Layout>
          </PrivateRoute>
        }
      />
      <Route
        path="/timetable"
        element={
          <PrivateRoute>
            <Layout>
              <Timetable />
            </Layout>
          </PrivateRoute>
        }
      />
      <Route
        path="/exams"
        element={
          <PrivateRoute>
            <Layout>
              <Exams />
            </Layout>
          </PrivateRoute>
        }
      />
      
      <Route path="/" element={<Navigate to={user ? `/${user.role}/dashboard` : '/login'} />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
        <Toaster position="top-right" />
      </Router>
    </AuthProvider>
  );
}

export default App;

