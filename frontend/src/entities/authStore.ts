import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User } from '../shared/api/types';
import { authApi } from '../shared/api';

interface AuthState {
  user: User | null;
  token: string | null;
  telegramId: string | null;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  setTelegramId: (id: string | null) => void;
  login: (telegramId: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: localStorage.getItem('token'),
      telegramId: localStorage.getItem('telegram_id'),
      setUser: (user) => set({ user }),
      setToken: (token) => {
        if (token) localStorage.setItem('token', token);
        else localStorage.removeItem('token');
        set({ token });
      },
      setTelegramId: (telegramId) => {
        if (telegramId) localStorage.setItem('telegram_id', telegramId);
        else localStorage.removeItem('telegram_id');
        set({ telegramId });
      },
      login: async (telegramId) => {
        try {
          const response = await authApi.login(telegramId);
          const token = response.data.access;
          localStorage.setItem('token', token);
          localStorage.setItem('telegram_id', telegramId);
          set({
            token,
            telegramId
          });
        } catch (error) {
          console.error('Login failed', error);
          throw error;
        }
      },
      logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('telegram_id');
        set({ user: null, token: null, telegramId: null });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ token: state.token, telegramId: state.telegramId }),
    }
  )
);
