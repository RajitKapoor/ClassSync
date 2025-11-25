import { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const Exams = () => {
  const { user } = useAuth();
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExams();
  }, []);

  const fetchExams = async () => {
    try {
      const response = await api.get('/exams/');
      setExams(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching exams:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Exams</h1>
      
      <div className="space-y-4">
        {exams.map((exam) => (
          <div key={exam.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                  {exam.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mt-2">{exam.description}</p>
                <div className="mt-4 flex space-x-4 text-sm text-gray-500 dark:text-gray-400">
                  <span>Course: {exam.course?.code}</span>
                  <span>Duration: {exam.duration_minutes} minutes</span>
                  <span>Max Marks: {exam.max_marks}</span>
                </div>
                <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                  <span>
                    {new Date(exam.start_time).toLocaleString()} - {new Date(exam.end_time).toLocaleString()}
                  </span>
                </div>
              </div>
              <div className="flex flex-col items-end space-y-2">
                {exam.is_active && (
                  <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                    Active
                  </span>
                )}
                {exam.is_upcoming && (
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                    Upcoming
                  </span>
                )}
                {exam.is_ended && (
                  <span className="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm">
                    Ended
                  </span>
                )}
                {user?.is_student && exam.is_active && (
                  <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                    Take Exam
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Exams;

