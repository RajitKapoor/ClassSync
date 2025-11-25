import { useState, useEffect } from 'react';
import api from '../services/api';

const AdminDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/dashboard/admin/');
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
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Admin Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Students</h3>
          <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">
            {data?.stats?.total_students || 0}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Teachers</h3>
          <p className="text-3xl font-bold text-green-600 dark:text-green-400">
            {data?.stats?.total_teachers || 0}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Courses</h3>
          <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">
            {data?.stats?.total_courses || 0}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Assignments</h3>
          <p className="text-3xl font-bold text-orange-600 dark:text-orange-400">
            {data?.stats?.total_assignments || 0}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">Exams</h3>
          <p className="text-3xl font-bold text-red-600 dark:text-red-400">
            {data?.stats?.total_exams || 0}
          </p>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Recent Leave Requests</h2>
        <div className="space-y-3">
          {data?.recent_leaves?.map((leave) => (
            <div key={leave.id} className="border-b dark:border-gray-700 pb-2 flex justify-between">
              <div>
                <p className="font-semibold text-gray-900 dark:text-white">{leave.student}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {leave.leave_type} - {new Date(leave.start_date).toLocaleDateString()} to {new Date(leave.end_date).toLocaleDateString()}
                </p>
              </div>
              <span className={`px-3 py-1 rounded-full text-sm ${
                leave.status === 'approved' ? 'bg-green-100 text-green-800' :
                leave.status === 'rejected' ? 'bg-red-100 text-red-800' :
                'bg-yellow-100 text-yellow-800'
              }`}>
                {leave.status}
              </span>
            </div>
          ))}
          {(!data?.recent_leaves || data.recent_leaves.length === 0) && (
            <p className="text-gray-500 dark:text-gray-400">No pending leave requests</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;

