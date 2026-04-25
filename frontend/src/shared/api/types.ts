export interface User {
  id: number;
  username?: string;
  first_name: string;
  last_name?: string;
  timezone: string;
}

export interface AuthResponse {
  refresh: string;
  access: string;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  owner: number;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  project: string;
  creator: number;
  assignee?: number;
  title: string;
  description?: string;
  status: 'todo' | 'in_progress' | 'done';
  deadline?: string;
  created_at: string;
  updated_at: string;
}

export interface FocusSession {
  id: string;
  user: number;
  task?: string;
  start_time: string;
  end_time?: string;
  duration: number;
  interruptions_count: number;
  context: 'work' | 'study' | 'custom';
  created_at: string;
}

export interface DailyStat {
  date: string;
  focus_time: number;
  tasks_done: number;
}

export interface DashboardStats {
  last_7_days: DailyStat[];
  last_30_days: DailyStat[];
}

export interface TodayStats {
  total_focus_time: number;
  completed_tasks_count: number;
  interruptions_count: number;
}
