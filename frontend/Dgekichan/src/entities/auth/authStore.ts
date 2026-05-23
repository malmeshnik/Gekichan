import { create } from "zustand";
import { apiClient } from "@/shared/api/client";
import axios from "axios";

interface User {
  id: number;
  username: string | null;
  first_name: string;
  last_name: string | null;
  avatar_url: string | null;
  daily_goal: number;
  streak: number;
  created_at: string;
  style?: {
    slug: string;
    title: string;
    description: string;
    icon: string;
  };
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isLoading: boolean;
  login: () => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  accessToken: localStorage.getItem("accessToken"),
  isLoading: false,

  login: async () => {
    set({ isLoading: true });
    try {
      const tg = window.Telegram?.WebApp;
      const initData = tg?.initData;

      const payload: any = {};

      if (initData) {
        payload.init_data = initData;
      } else {
        // Fallback for development
        const savedId = localStorage.getItem("telegramId") || "123456789";
        payload.telegram_id = parseInt(savedId);
        payload.first_name = "Dev User";
      }

      const response = await apiClient.post("/auth/telegram/", payload);
      const { access, user } = response.data;

      localStorage.setItem("accessToken", access);
      localStorage.setItem("telegramId", user.id.toString());

      set({ user, accessToken: access, isLoading: false });

      if (tg) {
        tg.ready();
        tg.expand();
      }
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("telegramId");
    set({ user: null, accessToken: null });
  },

  fetchMe: async () => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get("/users/me/");
      set({ user: response.data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      // If unauthorized, clear local state
      if (axios.isAxiosError(error) && error.response?.status === 401) {
        localStorage.removeItem("accessToken");
        set({ accessToken: null, user: null });
      }
    }
  },
}));
