import { create } from "zustand";
import { apiClient } from "@/shared/api/client";

interface TodayStats {
  total_focus_time: number;
  completed_tasks_count: number;
  interruptions_count: number;
}

export interface ChartDataItem {
  label: string;
  date?: string;
  focus_time: number;
  tasks_done: number;
}

export interface ProductivityStats {
  tasks_created_today: number;
  tasks_completed_today: number;
  tasks_completed_yesterday: number;
  tasks_delta_percent: number;
  overdue_tasks: number;
  completion_rate: number;
  focus_today_seconds: number;
  focus_yesterday_seconds: number;
  focus_delta_percent: number;
  average_focus_session_seconds: number;
  best_focus_duration_seconds: number;
  active_members_count: number;
  focus_streak: number;
  task_streak: number;
  best_day: string | null;
  chart_data: ChartDataItem[];
  ai_insight: string | null;
}

interface StatsState {
  todayStats: TodayStats | null;
  productivityStats: ProductivityStats | null;
  isLoading: boolean;
  fetchTodayStats: () => Promise<void>;
  fetchProductivity: (params?: { period?: string; start?: string; end?: string }) => Promise<void>;
}

export const useStatsStore = create<StatsState>((set) => ({
  todayStats: null,
  productivityStats: null,
  isLoading: false,

  fetchTodayStats: async () => {
    try {
      const response = await apiClient.get("/analytics/today/");
      set({ todayStats: response.data });
    } catch (error) {
      console.error("Failed to fetch today stats", error);
    }
  },

  fetchProductivity: async (params) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get("/analytics/productivity/", { params });
      set({ productivityStats: response.data, isLoading: false });
    } catch (error) {
      console.error("Failed to fetch productivity", error);
      set({ isLoading: false });
    }
  },
}));
