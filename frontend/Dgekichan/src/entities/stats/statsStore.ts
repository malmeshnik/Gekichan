import { create } from "zustand";
import { apiClient } from "@/shared/api/client";

interface TodayStats {
  total_focus_time: number;
  completed_tasks_count: number;
  interruptions_count: number;
}

interface ProductivityStats {
    focus_today_seconds: number;
    focus_yesterday_seconds: number;
}

interface StatsState {
  todayStats: TodayStats | null;
  productivityStats: ProductivityStats | null;
  isLoading: boolean;
  fetchTodayStats: () => Promise<void>;
  fetchProductivity: () => Promise<void>;
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

  fetchProductivity: async () => {
    try {
        const response = await apiClient.get("/analytics/productivity/");
        set({ productivityStats: response.data });
    } catch (error) {
        console.error("Failed to fetch productivity", error);
    }
  }
}));
