import React, { Suspense, lazy, useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { BottomNavigation } from '../shared/ui/BottomNavigation';
import { useAuthStore } from '../entities/authStore';
import { ToastContainer } from '../shared/ui/Toast';
import './styles/App.css';

const DashboardPage = lazy(() => import('../pages/DashboardPage').then(m => ({ default: m.DashboardPage })));
const TasksPage = lazy(() => import('../pages/TasksPage').then(m => ({ default: m.TasksPage })));
const TimerPage = lazy(() => import('../pages/TimerPage').then(m => ({ default: m.TimerPage })));
const StatsPage = lazy(() => import('../pages/StatsPage').then(m => ({ default: m.StatsPage })));
const ProjectsPage = lazy(() => import('../pages/ProjectsPage').then(m => ({ default: m.ProjectsPage })));
const SettingsPage = lazy(() => import('../pages/SettingsPage').then(m => ({ default: m.SettingsPage })));

const Loading = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="w-8 h-8 border-4 border-primary-start border-t-transparent rounded-full animate-spin" />
  </div>
);

function App() {
  const { token, telegramId, login } = useAuthStore();
  const [isReady, setIsReady] = useState(false);
  const [devTelegramId, setDevTelegramId] = useState('');

  useEffect(() => {
    const initAuth = async () => {
      const tg = (window as any).Telegram?.WebApp;
      const tgUser = tg?.initDataUnsafe?.user;

      if (tgUser?.id) {
        await login(tgUser.id.toString());
        setIsReady(true);
      } else if (token && telegramId) {
        setIsReady(true);
      } else {
        setIsReady(false);
      }
    };

    initAuth();
  }, [login, token, telegramId]);

  const handleDevLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (devTelegramId) {
      await login(devTelegramId);
      setIsReady(true);
    }
  };

  if (!isReady && !token) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center p-md">
        <h1 className="text-xl font-bold mb-lg">Dev Mode Auth</h1>
        <form onSubmit={handleDevLogin} className="w-full max-w-xs flex flex-col gap-md">
          <input
            type="text"
            placeholder="Enter Telegram ID"
            value={devTelegramId}
            onChange={(e) => setDevTelegramId(e.target.value)}
            className="w-full p-md bg-card border border-border rounded-xl text-text-primary"
          />
          <button
            type="submit"
            className="w-full p-md bg-primary-start text-white rounded-xl font-bold"
          >
            Login
          </button>
        </form>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-text-primary overflow-x-hidden">
        <ToastContainer />
        <Suspense fallback={<Loading />}>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="/timer" element={<TimerPage />} />
            <Route path="/stats" element={<StatsPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </Suspense>
        <BottomNavigation />
      </div>
    </BrowserRouter>
  );
}

export default App;
