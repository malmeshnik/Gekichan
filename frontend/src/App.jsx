import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AuthProvider from './components/AuthProvider';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import TimerPage from './pages/TimerPage';
import TasksPage from './pages/TasksPage';
import StatsPage from './pages/StatsPage';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/timer" element={<TimerPage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="/stats" element={<StatsPage />} />
          </Routes>
        </Layout>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
