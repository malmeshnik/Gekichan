import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, Square, Loader } from 'lucide-react';
import api from '../api/client';
import { useSessionStore, useTaskStore } from '../store';

const TimerPage = () => {
  const { currentSession, timerSeconds, isActive, tick, syncWithBackend } = useSessionStore();
  const { tasks, setTasks } = useTaskStore();
  const [loading, setLoading] = useState(true);
  const [selectedTaskId, setSelectedTaskId] = useState('');
  const timerRef = useRef(null);

  useEffect(() => {
    const initTimer = async () => {
      try {
        const [sessionRes, tasksRes] = await Promise.all([
          api.get('/sessions/').then(res => {
            // Find active session
            const results = res.data.results || res.data;
            return { data: results.find(s => !s.end_time) || null };
          }).catch(() => ({ data: null })),
          api.get('/tasks/?status=todo,in_progress')
        ]);

        syncWithBackend(sessionRes.data);
        setTasks(tasksRes.data.results || tasksRes.data);

        if (sessionRes.data?.task) {
          setSelectedTaskId(sessionRes.data.task);
        }
      } catch (error) {
        console.error('Failed to init timer', error);
      } finally {
        setLoading(false);
      }
    };
    initTimer();
  }, []);

  useEffect(() => {
    if (isActive) {
      timerRef.current = setInterval(() => tick(), 1000);
    } else {
      clearInterval(timerRef.current);
    }
    return () => clearInterval(timerRef.current);
  }, [isActive]);

  const handleStart = async () => {
    try {
      const response = await api.post('/sessions/start/', {
        task: selectedTaskId || null
      });
      syncWithBackend(response.data);
    } catch (error) {
      alert('Failed to start session');
    }
  };

  const handlePause = async () => {
    if (!currentSession) return;
    try {
      await api.patch(`/sessions/${currentSession.id}/pause/`);
      // Interruption logged
    } catch (error) {
      alert('Failed to pause');
    }
  };

  const handleStop = async () => {
    if (!currentSession) return;
    try {
      await api.patch(`/sessions/${currentSession.id}/stop/`);
      syncWithBackend(null);
    } catch (error) {
      alert('Failed to stop session');
    }
  };

  const formatTime = (totalSeconds) => {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) return <div className="flex justify-center p-10"><Loader className="animate-spin" /></div>;

  return (
    <div className="p-4 flex flex-col items-center">
      <h1 className="text-2xl font-bold mb-8">Focus Timer</h1>

      <div className="w-64 h-64 rounded-full border-8 border-blue-600 flex items-center justify-center mb-8 shadow-inner">
        <span className="text-5xl font-mono font-bold text-gray-800">
          {formatTime(timerSeconds)}
        </span>
      </div>

      {!isActive ? (
        <div className="w-full max-w-xs space-y-4">
          <select
            value={selectedTaskId}
            onChange={(e) => setSelectedTaskId(e.target.value)}
            className="w-full p-3 border rounded-lg bg-white"
          >
            <option value="">No specific task</option>
            {tasks.map(t => (
              <option key={t.id} value={t.id}>{t.title}</option>
            ))}
          </select>
          <button
            onClick={handleStart}
            className="w-full bg-blue-600 text-white p-4 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg"
          >
            <Play fill="currentColor" /> Start Session
          </button>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-6">
          {currentSession?.task_title && (
            <p className="text-gray-600">
              Focusing on: <span className="font-semibold">{currentSession.task_title}</span>
            </p>
          )}
          <div className="flex gap-4">
            <button
              onClick={handlePause}
              className="w-20 h-20 bg-yellow-500 text-white rounded-full flex items-center justify-center shadow-lg active:scale-95 transition-transform"
              title="Log Interruption"
            >
              <Pause fill="currentColor" />
            </button>
            <button
              onClick={handleStop}
              className="w-20 h-20 bg-red-600 text-white rounded-full flex items-center justify-center shadow-lg active:scale-95 transition-transform"
            >
              <Square fill="currentColor" />
            </button>
          </div>
          <p className="text-xs text-gray-400">Pause button logs an interruption</p>
        </div>
      )}
    </div>
  );
};

export default TimerPage;
