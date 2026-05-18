import { create } from "zustand";
import { apiClient } from "@/shared/api/client";

export interface Task {
  id: number;
  title: string;
  status: "todo" | "in_progress" | "done";
  priority: "low" | "medium" | "high";
  project_name?: string;
}

interface TaskState {
  tasks: Task[];
  isLoading: boolean;
  fetchTasks: () => Promise<void>;
}

export const useTaskStore = create<TaskState>((set) => ({
  tasks: [],
  isLoading: false,

  fetchTasks: async () => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get("/tasks/");
      set({ tasks: response.data.results || response.data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      console.error("Failed to fetch tasks", error);
    }
  },
}));
