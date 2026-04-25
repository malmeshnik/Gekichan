import api from '@/shared/api/client';
import * as Types from '@/shared/api/types';

export const authApi = {
  login: (telegramId: string) =>
    api.post<Types.AuthResponse>('auth/telegram/', { telegram_id: telegramId }),
};

export const projectsApi = {
  list: () => api.get<Types.Project[]>('projects/'),
  create: (data: Partial<Types.Project>) => api.post<Types.Project>('projects/', data),
};

export const tasksApi = {
  list: () => api.get<Types.Task[]>('tasks/'),
  create: (data: Partial<Types.Task>) => api.post<Types.Task>('tasks/', data),
  update: (id: string, data: Partial<Types.Task>) => api.patch<Types.Task>(`tasks/${id}/`, data),
};

export const sessionsApi = {
  list: () => api.get<Types.FocusSession[]>('sessions/'),
  start: (data: { task?: string; context?: string }) =>
    api.post<Types.FocusSession>('sessions/start/', data),
  pause: (id: string) => api.patch<Types.FocusSession>(`sessions/${id}/pause/`),
  stop: (id: string) => api.patch<Types.FocusSession>(`sessions/${id}/stop/`),
};

export const statsApi = {
  today: () => api.get<Types.TodayStats>('stats/today/'),
  dashboard: () => api.get<Types.DashboardStats>('stats/dashboard/'),
};

export * from '@/shared/api/types';
