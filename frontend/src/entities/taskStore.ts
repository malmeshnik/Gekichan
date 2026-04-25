import { create } from 'zustand';
import { Task, Project } from '@/shared/api/types';
import { tasksApi, projectsApi } from '@/shared/api';
import { useStatsStore } from '@/entities/statsStore';

interface TaskState {
  tasks: Task[];
  projects: Project[];
  isLoading: boolean;
  error: string | null;
  fetchTasks: () => Promise<void>;
  fetchProjects: () => Promise<void>;
  addTask: (task: Partial<Task>) => Promise<void>;
  updateTaskStatus: (id: string, status: Task['status']) => Promise<void>;
  addProject: (project: Partial<Project>) => Promise<void>;
}

export const useTaskStore = create<TaskState>((set, get) => ({
  tasks: [],
  projects: [],
  isLoading: false,
  error: null,

  fetchTasks: async () => {
    set({ isLoading: true });
    try {
      const response = await tasksApi.list();
      set({ tasks: response.data, isLoading: false });
    } catch (error) {
      set({ error: 'Failed to fetch tasks', isLoading: false });
    }
  },

  fetchProjects: async () => {
    set({ isLoading: true });
    try {
      const response = await projectsApi.list();
      set({ projects: response.data, isLoading: false });
    } catch (error) {
      set({ error: 'Failed to fetch projects', isLoading: false });
    }
  },

  addTask: async (taskData) => {
    try {
      const response = await tasksApi.create(taskData);
      set((state) => ({ tasks: [response.data, ...state.tasks] }));
      // Refresh stats
      useStatsStore.getState().fetchTodayStats();
    } catch (error) {
      console.error('Failed to add task', error);
    }
  },

  updateTaskStatus: async (id, status) => {
    try {
      const response = await tasksApi.update(id, { status });
      set((state) => ({
        tasks: state.tasks.map((t) => (t.id === id ? response.data : t)),
      }));
      // Refresh stats
      useStatsStore.getState().fetchTodayStats();
      useStatsStore.getState().fetchDashboardStats();
    } catch (error) {
      console.error('Failed to update task status', error);
    }
  },

  addProject: async (projectData) => {
    try {
      const response = await projectsApi.create(projectData);
      set((state) => ({ projects: [response.data, ...state.projects] }));
    } catch (error) {
      console.error('Failed to add project', error);
    }
  },
}));
