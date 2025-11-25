import { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const Timetable = () => {
  const { user } = useAuth();
  const [timetable, setTimetable] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTimetable();
  }, []);

  const fetchTimetable = async () => {
    try {
      const response = await api.get('/timetable/');
      setTimetable(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching timetable:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    try {
      await api.post('/timetable/generate/', {
        semester: 1,
        academic_year: '2024-2025',
      });
      fetchTimetable();
    } catch (error) {
      console.error('Error generating timetable:', error);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'];
  const groupedByDay = days.map(day => ({
    day,
    classes: timetable.filter(cls => cls.time_slot?.day === day),
  }));

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Timetable</h1>
        {user?.is_admin && (
          <button
            onClick={handleGenerate}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Generate Timetable
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {groupedByDay.map(({ day, classes }) => (
          <div key={day} className="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
            <h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white capitalize">
              {day}
            </h3>
            <div className="space-y-2">
              {classes.length > 0 ? (
                classes.map((cls) => (
                  <div key={cls.id} className="border-l-4 border-blue-500 p-2 bg-gray-50 dark:bg-gray-700 rounded">
                    <p className="font-semibold text-sm text-gray-900 dark:text-white">
                      {cls.course?.code}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {cls.time_slot?.start_time} - {cls.time_slot?.end_time}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {cls.room?.name}
                    </p>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 dark:text-gray-400 text-sm">No classes</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Timetable;

