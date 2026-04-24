import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  setUser: (user) => set({ user }),
  setToken: (token) => {
    localStorage.setItem('token', token);
    set({ token });
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ user: null, token: null });
  },
}));

export const useTaskStore = create((set) => ({
  tasks: [],
  projects: [],
  setTasks: (tasks) => set({ tasks }),
  setProjects: (projects) => set({ projects }),
  addTask: (task) => set((state) => ({ tasks: [task, ...state.tasks] })),
}));

export const useSessionStore = create((set, get) => ({
  currentSession: null,
  timerSeconds: 0,
  isActive: false,
  setCurrentSession: (session) => set({ currentSession: session }),
  setTimerSeconds: (seconds) => set({ timerSeconds: seconds }),
  setIsActive: (isActive) => set({ isActive }),

  tick: () => {
    if (get().isActive) {
      set((state) => ({ timerSeconds: state.timerSeconds + 1 }));
    }
  },

  syncWithBackend: (session) => {
    if (!session) {
      set({ currentSession: null, isActive: false, timerSeconds: 0 });
      return;
    }

    const startTime = new Date(session.start_time).getTime();
    const now = new Date().getTime();
    const elapsedSeconds = Math.floor((now - startTime) / 1000);

    set({
      currentSession: session,
      isActive: !session.end_time,
      timerSeconds: session.duration || elapsedSeconds
    });
  }
}));
