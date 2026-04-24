import { create } from 'zustand';
import { User, Task, Project, FocusSession } from './types';

interface AuthState {
  user: User | null;
  token: string | null;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  setUser: (user) => set({ user }),
  setToken: (token) => {
    if (token) localStorage.setItem('token', token);
    else localStorage.removeItem('token');
    set({ token });
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ user: null, token: null });
  },
}));

interface TaskState {
  tasks: Task[];
  projects: Project[];
  setTasks: (tasks: Task[]) => void;
  setProjects: (projects: Project[]) => void;
  addTask: (task: Task) => void;
}

export const useTaskStore = create<TaskState>((set) => ({
  tasks: [],
  projects: [],
  setTasks: (tasks) => set({ tasks }),
  setProjects: (projects) => set({ projects }),
  addTask: (task) => set((state) => ({ tasks: [task, ...state.tasks] })),
}));

interface SessionState {
  currentSession: FocusSession | null;
  remainingSeconds: number;
  isActive: boolean;
  lastTickTimestamp: number | null;
  setCurrentSession: (session: FocusSession | null) => void;
  setRemainingSeconds: (seconds: number) => void;
  setIsActive: (isActive: boolean) => void;
  syncWithBackend: (session: FocusSession | null) => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  currentSession: null,
  remainingSeconds: 25 * 60,
  isActive: false,
  lastTickTimestamp: null,
  setCurrentSession: (session) => set({ currentSession: session }),
  setRemainingSeconds: (seconds) => set({ remainingSeconds: seconds }),
  setIsActive: (isActive) => set({
    isActive,
    lastTickTimestamp: isActive ? Date.now() : null
  }),

  syncWithBackend: (session) => {
    if (!session) {
      set({ currentSession: null, isActive: false, remainingSeconds: 25 * 60 });
      return;
    }

    const startTime = new Date(session.start_time).getTime();
    const now = new Date().getTime();
    const elapsedSeconds = Math.floor((now - startTime) / 1000);
    const duration = 25 * 60; // Default

    set({
      currentSession: session,
      isActive: !session.end_time,
      remainingSeconds: session.end_time ? 0 : Math.max(0, duration - elapsedSeconds)
    });
  }
}));
