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
  tasks_completed: number;
  productivity_score: number;
}

export interface ProductivityStats {
  focus_streak: number;
  tasks_streak: number;
  best_day: {
    date: string;
    score: number;
  } | null;
  chart_data: ChartDataItem[];
  ai_insight: string | null;
  tasks_completed_today?: number;
  focus_today_seconds?: number;
  focus_yesterday_seconds?: number;
  leaderboard?: any[];
  member_focus_stats?: any[];
}

interface StatsState {
  todayStats: TodayStats | null;
  productivityStats: ProductivityStats | null;
  isLoading: boolean;
  fetchTodayStats: () => Promise<void>;
  fetchProductivity: (params?: { period?: string; start?: string; end?: string; projectId?: number }) => Promise<void>;
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
      const url = params?.projectId
        ? `/analytics/projects/${params.projectId}/productivity/`
        : "/analytics/productivity/";
      const response = await apiClient.get(url, { params });
      set({ productivityStats: response.data, isLoading: false });
    } catch (error) {
      console.error("Failed to fetch productivity", error);
      set({ isLoading: false });
    }
  },
}));
