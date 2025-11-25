import { useState, useEffect } from 'react';
import api from '../services/api';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const StudentDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/dashboard/student/');
        setData(response.data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  const attendanceData = [
    { month: 'Jan', attendance: 85 },
    { month: 'Feb', attendance: 88 },
    { month: 'Mar', attendance: 82 },
    { month: 'Apr', attendance: 90 },
    { month: 'May', attendance: 87 },
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Student Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Attendance</h3>
          <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            {data?.attendance?.percent || 0}%
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Pending Assignments</h3>
          <p className="text-3xl font-bold text-orange-600 dark:text-orange-400">
            {data?.pending_assignments?.length || 0}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Unread Notifications</h3>
          <p className="text-3xl font-bold text-red-600 dark:text-red-400">
            {data?.unread_notifications || 0}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Upcoming Classes</h2>
          <div className="space-y-3">
            {data?.upcoming_classes?.slice(0, 5).map((cls) => (
              <div key={cls.id} className="border-b dark:border-gray-700 pb-2">
                <p className="font-semibold text-gray-900 dark:text-white">{cls.course} - {cls.course_name}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {cls.day} {cls.time} - {cls.room}
                </p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Pending Assignments</h2>
          <div className="space-y-3">
            {data?.pending_assignments?.map((ass) => (
              <div key={ass.id} className="border-b dark:border-gray-700 pb-2">
                <p className="font-semibold text-gray-900 dark:text-white">{ass.title}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Due: {new Date(ass.deadline).toLocaleString()}
                  {ass.is_overdue && <span className="text-red-600 ml-2">(Overdue)</span>}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Attendance Trend</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={attendanceData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="attendance" stroke="#3b82f6" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default StudentDashboard;

