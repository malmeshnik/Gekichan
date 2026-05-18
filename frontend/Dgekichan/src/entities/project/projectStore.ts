import { create } from "zustand";
import { apiClient } from "@/shared/api/client";

export interface ProjectMember {
  id: number;
  user: number;
  user_detail?: {
    id: number;
    first_name: string;
    username: string;
    avatar_url?: string;
  };
  role: "owner" | "admin" | "member";
  label?: string;
}

export interface Project {
  id: number;
  name: string;
  description: string;
  owner: number;
  created_at: string;
  updated_at: string;
  members: ProjectMember[];
  members_count: number;
  tasks_count: number;
  overdue_tasks_count: number;
  active_members_count: number;
  in_progress_tasks_count: number;
  done_tasks_count: number;
  total_focus_time: number;
  last_activity: string | null;
}

interface ProjectState {
  projects: Project[];
  isLoading: boolean;
  fetchProjects: () => Promise<void>;
  createProject: (data: Partial<Project>) => Promise<Project>;
  updateProject: (id: number, data: Partial<Project>) => Promise<void>;
  deleteProject: (id: number) => Promise<void>;
  addMember: (projectId: number, username: string) => Promise<void>;
  updateMember: (projectId: number, memberId: number, data: Partial<ProjectMember>) => Promise<void>;
  removeMember: (projectId: number, memberId: number) => Promise<void>;
}

export const useProjectStore = create<ProjectState>((set, get) => ({
  projects: [],
  isLoading: false,

  fetchProjects: async () => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get("/projects/");
      const projects = response.data.results || response.data;
      set({ projects, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      console.error("Failed to fetch projects", error);
    }
  },

  createProject: async (data) => {
    try {
      const response = await apiClient.post("/projects/", data);
      set({ projects: [response.data, ...get().projects] });
      return response.data;
    } catch (error) {
      console.error("Failed to create project", error);
      throw error;
    }
  },

  updateProject: async (id, data) => {
    try {
      const response = await apiClient.patch(`/projects/${id}/`, data);
      set({
        projects: get().projects.map((p) => (p.id === id ? response.data : p)),
      });
    } catch (error) {
      console.error("Failed to update project", error);
      throw error;
    }
  },

  deleteProject: async (id) => {
    try {
      await apiClient.delete(`/projects/${id}/`);
      set({
        projects: get().projects.filter((p) => p.id !== id),
      });
    } catch (error) {
      console.error("Failed to delete project", error);
      throw error;
    }
  },

  addMember: async (projectId, username) => {
    try {
      await apiClient.post(`/projects/${projectId}/add_member/`, { username });
      const response = await apiClient.get(`/projects/${projectId}/`);
      set({
        projects: get().projects.map((p) => (p.id === projectId ? response.data : p)),
      });
    } catch (error) {
      console.error("Failed to add member", error);
      throw error;
    }
  },

  updateMember: async (projectId, memberId, data) => {
    try {
        await apiClient.patch(`/projects/${projectId}/members/${memberId}/`, data);
        const response = await apiClient.get(`/projects/${projectId}/`);
        set({
          projects: get().projects.map((p) => (p.id === projectId ? response.data : p)),
        });
    } catch (error) {
        console.error("Failed to update member", error);
        throw error;
    }
  },

  removeMember: async (projectId, memberId) => {
    try {
        await apiClient.delete(`/projects/${projectId}/members/${memberId}/`);
        const response = await apiClient.get(`/projects/${projectId}/`);
        set({
          projects: get().projects.map((p) => (p.id === projectId ? response.data : p)),
        });
    } catch (error) {
        console.error("Failed to remove member", error);
        throw error;
    }
  }
}));
