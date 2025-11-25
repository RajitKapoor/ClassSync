import { useState, useEffect } from 'react';
import api from '../services/api';

const TeacherDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/dashboard/teacher/');
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

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Teacher Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Courses Taught</h3>
          <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            {data?.stats?.courses_taught || 0}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Total Students</h3>
          <p className="text-3xl font-bold text-green-600 dark:text-green-400">
            {data?.stats?.total_students || 0}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Pending Grading</h3>
          <p className="text-3xl font-bold text-orange-600 dark:text-orange-400">
            {data?.stats?.pending_grading_count || 0}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Today's Classes</h2>
          <div className="space-y-3">
            {data?.today_classes?.map((cls) => (
              <div key={cls.id} className="border-b dark:border-gray-700 pb-2">
                <p className="font-semibold text-gray-900 dark:text-white">{cls.course} - {cls.course_name}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {cls.time} - {cls.room}
                </p>
              </div>
            ))}
            {(!data?.today_classes || data.today_classes.length === 0) && (
              <p className="text-gray-500 dark:text-gray-400">No classes today</p>
            )}
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Pending Grading</h2>
          <div className="space-y-3">
            {data?.pending_grading?.map((sub) => (
              <div key={sub.id} className="border-b dark:border-gray-700 pb-2">
                <p className="font-semibold text-gray-900 dark:text-white">{sub.assignment}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Student: {sub.student} - {new Date(sub.submitted_at).toLocaleDateString()}
                  {sub.is_late && <span className="text-red-600 ml-2">(Late)</span>}
                </p>
              </div>
            ))}
            {(!data?.pending_grading || data.pending_grading.length === 0) && (
              <p className="text-gray-500 dark:text-gray-400">No pending grading</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeacherDashboard;

