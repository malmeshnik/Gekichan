import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { HomePage } from "@/pages/home";
import { LoginPage } from "@/pages/login/login-page";
import { ProjectsPage } from "@/pages/projects/projects-page";
import { TasksPage } from "@/pages/tasks/tasks-page";
import { StatsPage } from "@/pages/stats/stats-page";
import { PlaceholderPage } from "@/pages/placeholder";
import { useAuthStore } from "@/entities/auth/authStore";
import { useEffect } from "react";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { accessToken, user, fetchMe } = useAuthStore();

  useEffect(() => {
    if (accessToken && !user) {
      fetchMe();
    }
  }, [accessToken, user, fetchMe]);

  if (!accessToken) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/tasks"
          element={
            <ProtectedRoute>
              <TasksPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/projects"
          element={
            <ProtectedRoute>
              <ProjectsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/stats"
          element={
            <ProtectedRoute>
              <StatsPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
