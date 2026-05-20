import { create } from "zustand";
import { apiClient } from "@/shared/api/client";

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: "todo" | "in_progress" | "done";
  priority: "low" | "medium" | "high";
  project?: number;
  project_name?: string;
  focus_time?: number;
  deadline?: string;
  assignee?: number;
}

interface TaskState {
  tasks: Task[];
  isLoading: boolean;
  fetchTasks: (params?: Record<string, string | number | null>) => Promise<void>;
  createTask: (data: Partial<Task>) => Promise<void>;
  updateTask: (id: number, data: Partial<Task>) => Promise<void>;
  deleteTask: (id: number) => Promise<void>;
}

export const useTaskStore = create<TaskState>((set, get) => ({
  tasks: [],
  isLoading: false,

  fetchTasks: async (params = {}) => {
    set({ isLoading: true });
    try {
      // Convert params to query string
      const queryParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== null && value !== undefined) {
            queryParams.append(key, String(value));
        }
      });

      const response = await apiClient.get(`/tasks/?${queryParams.toString()}`);
      set({ tasks: response.data.results || response.data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      console.error("Failed to fetch tasks", error);
    }
  },

  createTask: async (data) => {
    try {
      const response = await apiClient.post("/tasks/", data);
      set({ tasks: [response.data, ...get().tasks] });
    } catch (error) {
      console.error("Failed to create task", error);
      throw error;
    }
  },

  updateTask: async (id, data) => {
    try {
      const response = await apiClient.patch(`/tasks/${id}/`, data);
      set({
        tasks: get().tasks.map((t) => (t.id === id ? response.data : t)),
      });
    } catch (error) {
      console.error("Failed to update task", error);
      throw error;
    }
  },

  deleteTask: async (id) => {
    try {
      await apiClient.delete(`/tasks/${id}/`);
      set({
        tasks: get().tasks.filter((t) => t.id !== id),
      });
    } catch (error) {
      console.error("Failed to delete task", error);
      throw error;
    }
  },
}));
