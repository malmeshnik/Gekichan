import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';
import { Clock, CheckCircle, AlertCircle, Play } from 'lucide-react';

const Dashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const [statsRes, tasksRes] = await Promise.all([
          api.get('/stats/today/'),
          api.get('/tasks/?status=todo&limit=3')
        ]);
        setStats(statsRes.data);
        setTasks(tasksRes.data.results || tasksRes.data);
      } catch (error) {
        console.error('Dashboard fetch failed', error);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  const formatDuration = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${h}h ${m}m`;
  };

  if (loading) return <div className="p-4">Loading dashboard...</div>;

  return (
    <div className="p-4 space-y-6">
      <header>
        <h1 className="text-2xl font-bold">Hello!</h1>
        <p className="text-gray-500 text-sm">Here's your productivity overview for today.</p>
      </header>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-blue-50 p-4 rounded-2xl border border-blue-100">
          <div className="flex items-center gap-2 text-blue-600 mb-2">
            <Clock size={16} />
            <span className="text-xs font-semibold uppercase">Focus Time</span>
          </div>
          <div className="text-2xl font-bold text-blue-900">
            {formatDuration(stats?.total_focus_time || 0)}
          </div>
        </div>
        <div className="bg-green-50 p-4 rounded-2xl border border-green-100">
          <div className="flex items-center gap-2 text-green-600 mb-2">
            <CheckCircle size={16} />
            <span className="text-xs font-semibold uppercase">Completed</span>
          </div>
          <div className="text-2xl font-bold text-green-900">
            {stats?.completed_tasks_count || 0}
          </div>
        </div>
      </div>

      <section>
        <div className="flex justify-between items-center mb-3">
          <h2 className="font-bold text-lg">Next Tasks</h2>
          <button onClick={() => navigate('/tasks')} className="text-blue-600 text-sm">View All</button>
        </div>
        <div className="space-y-2">
          {tasks.slice(0, 3).map(task => (
            <div key={task.id} className="p-3 bg-white border rounded-xl flex items-center gap-3">
              <div className="w-2 h-2 rounded-full bg-gray-300" />
              <span className="text-sm font-medium">{task.title}</span>
            </div>
          ))}
          {tasks.length === 0 && <p className="text-gray-400 text-sm italic">No pending tasks.</p>}
        </div>
      </section>

      <button
        onClick={() => navigate('/timer')}
        className="w-full bg-blue-600 text-white p-4 rounded-2xl font-bold flex items-center justify-center gap-2 shadow-lg shadow-blue-200 sticky bottom-4"
      >
        <Play fill="currentColor" size={20} /> Start Session
      </button>
    </div>
  );
};

export default Dashboard;
