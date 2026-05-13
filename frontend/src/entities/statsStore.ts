import { create } from 'zustand';
import { TodayStats, DashboardStats } from '../shared/api/types';
import { statsApi } from '../shared/api';

interface StatsState {
  today: TodayStats | null;
  dashboard: DashboardStats | null;
  isLoading: boolean;
  fetchTodayStats: () => Promise<void>;
  fetchDashboardStats: () => Promise<void>;
}

export const useStatsStore = create<StatsState>((set) => ({
  today: null,
  dashboard: null,
  isLoading: false,

  fetchTodayStats: async () => {
    set({ isLoading: true });
    try {
      const response = await statsApi.today();
      set({ today: response.data, isLoading: false });
    } catch (error) {
      console.error('Failed to fetch today stats', error);
      set({ isLoading: false });
    }
  },

  fetchDashboardStats: async () => {
    set({ isLoading: true });
    try {
      const response = await statsApi.dashboard();
      set({ dashboard: response.data, isLoading: false });
    } catch (error) {
      console.error('Failed to fetch dashboard stats', error);
      set({ isLoading: false });
    }
  },
}));
