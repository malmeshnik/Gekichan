import { create } from "zustand";
import { apiClient } from "@/shared/api/client";

interface FocusSession {
  id: number;
  status: "active" | "paused" | "completed";
  start_time: string;
  last_paused_at: string | null;
  total_paused_duration: number;
  task: number | null;
  task_title?: string;
}

interface SessionState {
  currentSession: FocusSession | null;
  isLoading: boolean;
  fetchActiveSession: () => Promise<void>;
  startSession: (taskId: number) => Promise<void>;
  pauseSession: () => Promise<void>;
  resumeSession: () => Promise<void>;
  stopSession: () => Promise<void>;
}

export const useSessionStore = create<SessionState>((set, get) => ({
  currentSession: null,
  isLoading: false,

  fetchActiveSession: async () => {
    try {
      const response = await apiClient.get("/sessions/");
      const sessions = response.data.results || response.data;
      const active = sessions.find((s: FocusSession) => s.status !== "completed");
      set({ currentSession: active || null });
    } catch (error) {
      console.error("Failed to fetch sessions", error);
    }
  },

  startSession: async (taskId: number) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.post("/sessions/start/", { task: taskId });
      set({ currentSession: response.data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  pauseSession: async () => {
    const { currentSession } = get();
    if (!currentSession) return;
    try {
      const response = await apiClient.patch(`/sessions/${currentSession.id}/pause/`);
      set({ currentSession: response.data });
    } catch (error) {
      console.error("Failed to pause session", error);
    }
  },

  resumeSession: async () => {
    const { currentSession } = get();
    if (!currentSession) return;
    try {
      const response = await apiClient.patch(`/sessions/${currentSession.id}/resume/`);
      set({ currentSession: response.data });
    } catch (error) {
      console.error("Failed to resume session", error);
    }
  },

  stopSession: async () => {
    const { currentSession } = get();
    if (!currentSession) return;
    try {
      await apiClient.patch(`/sessions/${currentSession.id}/stop/`);
      set({ currentSession: null });
    } catch (error) {
      console.error("Failed to stop session", error);
    }
  },
}));
