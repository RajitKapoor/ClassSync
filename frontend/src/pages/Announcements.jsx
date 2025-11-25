import { useState, useEffect } from 'react';
import api from '../services/api';

const Announcements = () => {
  const [announcements, setAnnouncements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnnouncements();
  }, []);

  const fetchAnnouncements = async () => {
    try {
      const response = await api.get('/announcements/');
      setAnnouncements(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching announcements:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Announcements</h1>
      
      <div className="space-y-4">
        {announcements.map((announcement) => (
          <div
            key={announcement.id}
            className={`bg-white dark:bg-gray-800 rounded-lg shadow p-6 ${
              announcement.is_pinned ? 'border-l-4 border-blue-500' : ''
            }`}
          >
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                  {announcement.title}
                  {announcement.is_pinned && (
                    <span className="ml-2 text-blue-600">📌</span>
                  )}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mt-2">{announcement.content}</p>
              </div>
              <span
                className={`px-3 py-1 rounded-full text-sm ${
                  announcement.priority === 'urgent' ? 'bg-red-100 text-red-800' :
                  announcement.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                  announcement.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}
              >
                {announcement.priority}
              </span>
            </div>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-4">
              {new Date(announcement.created_at).toLocaleString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Announcements;

