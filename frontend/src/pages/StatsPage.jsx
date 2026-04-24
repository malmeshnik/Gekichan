import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { format } from 'date-fns';

const StatsPage = () => {
  const [today, setToday] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [todayRes, dashboardRes] = await Promise.all([
          api.get('/stats/today/'),
          api.get('/stats/dashboard/')
        ]);
        setToday(todayRes.data);
        setHistory(dashboardRes.data.last_7_days || []);
      } catch (error) {
        console.error('Stats fetch failed', error);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const formatTime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${h}h ${m}m`;
  };

  if (loading) return <div className="p-4 text-center">Loading stats...</div>;

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold">Analytics</h1>

      <section className="bg-white p-5 rounded-2xl border shadow-sm">
        <h2 className="text-gray-500 text-xs font-semibold uppercase mb-4">Today's Performance</h2>
        <div className="flex justify-between items-end">
          <div>
            <div className="text-3xl font-bold">{today?.productivity_score || 0}</div>
            <div className="text-sm text-gray-500">Productivity Score</div>
          </div>
          <div className="text-right">
            <div className="font-semibold text-blue-600">{formatTime(today?.total_focus_time || 0)}</div>
            <div className="text-xs text-gray-400">Total Focus</div>
          </div>
        </div>
      </section>

      <section>
        <h2 className="font-bold text-lg mb-4">Last 7 Days</h2>
        <div className="space-y-3">
          {history.length > 0 ? (
            history.slice().reverse().map(day => (
              <div key={day.date} className="flex items-center justify-between p-4 bg-white border rounded-xl shadow-sm">
                <div>
                  <div className="font-bold">{format(new Date(day.date), 'EEE, MMM d')}</div>
                  <div className="text-xs text-gray-500 font-medium">{day.tasks_done || day.completed_tasks_count || 0} tasks completed</div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-blue-600">{formatTime(day.focus_time || day.total_focus_time || 0)}</div>
                  <div className="text-xs text-gray-400">Focus Time</div>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-400 text-center py-8 italic border rounded-xl border-dashed">No history available yet.</p>
          )}
        </div>
      </section>
    </div>
  );
};

export default StatsPage;
