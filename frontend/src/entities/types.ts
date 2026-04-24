export interface User {
  id: number;
  username?: string;
  first_name: string;
  last_name?: string;
  timezone: string;
}

export interface Project {
  id: string;
  name: string;
  description?: string;
  owner: number;
}

export interface Task {
  id: string;
  project: string;
  project_name?: string;
  title: string;
  description?: string;
  status: 'todo' | 'in_progress' | 'done';
  deadline?: string;
  assignee?: number;
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
}
