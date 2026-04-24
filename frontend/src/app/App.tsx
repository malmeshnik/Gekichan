import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { BottomNavigation } from '../shared/ui/BottomNavigation';
import './styles/App.css';

const DashboardPage = lazy(() => import('../pages/DashboardPage').then(m => ({ default: m.DashboardPage })));
const TasksPage = lazy(() => import('../pages/TasksPage').then(m => ({ default: m.TasksPage })));
const TimerPage = lazy(() => import('../pages/TimerPage').then(m => ({ default: m.TimerPage })));
const StatsPage = lazy(() => import('../pages/StatsPage').then(m => ({ default: m.StatsPage })));
const ProjectsPage = lazy(() => import('../pages/ProjectsPage').then(m => ({ default: m.ProjectsPage })));

const Loading = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="w-8 h-8 border-4 border-primary-start border-t-transparent rounded-full animate-spin" />
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-background text-text-primary overflow-x-hidden">
        <Suspense fallback={<Loading />}>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="/timer" element={<TimerPage />} />
            <Route path="/stats" element={<StatsPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
          </Routes>
        </Suspense>
        <BottomNavigation />
      </div>
    </BrowserRouter>
  );
}

export default App;
