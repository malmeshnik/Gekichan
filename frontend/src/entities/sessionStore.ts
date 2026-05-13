import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { FocusSession } from '../shared/api/types';
import { sessionsApi } from '../shared/api';
import { useStatsStore } from './statsStore';

interface SessionState {
  currentSession: FocusSession | null;
  elapsedSeconds: number;
  isActive: boolean;
  selectedTaskId: string | null;

  setSelectedTaskId: (id: string | null) => void;
  fetchActiveSession: () => Promise<void>;
  startSession: (context?: string) => Promise<void>;
  pauseSession: () => Promise<void>;
  stopSession: () => Promise<void>;
  tick: () => void;
}

export const useSessionStore = create<SessionState>()(
  persist(
    (set, get) => ({
      currentSession: null,
      elapsedSeconds: 0,
      isActive: false,
      selectedTaskId: null,

      setSelectedTaskId: (id) => set({ selectedTaskId: id }),

      fetchActiveSession: async () => {
        try {
          const response = await sessionsApi.list();
          const activeSession = response.data.find(s => !s.end_time);
          if (activeSession) {
            const startTime = new Date(activeSession.start_time).getTime();
            const now = Date.now();
            const elapsed = Math.floor((now - startTime) / 1000);

            set({
              currentSession: activeSession,
              isActive: true,
              elapsedSeconds: elapsed,
              selectedTaskId: activeSession.task || null
            });
          } else {
            set({ currentSession: null, isActive: false, elapsedSeconds: 0 });
          }
        } catch (error) {
          console.error('Failed to fetch active session', error);
        }
      },

      startSession: async (context = 'work') => {
        try {
          const { selectedTaskId } = get();
          const response = await sessionsApi.start({
            task: selectedTaskId || undefined,
            context
          });
          set({
            currentSession: response.data,
            isActive: true,
            elapsedSeconds: 0
          });
          // Refresh stats
          useStatsStore.getState().fetchTodayStats();
        } catch (error) {
          console.error('Failed to start session', error);
        }
      },

      pauseSession: async () => {
        const { currentSession } = get();
        if (!currentSession) return;
        try {
          const response = await sessionsApi.pause(currentSession.id);
          set({ currentSession: response.data });
          // Refresh stats
          useStatsStore.getState().fetchTodayStats();
        } catch (error) {
          console.error('Failed to pause session', error);
        }
      },

      stopSession: async () => {
        const { currentSession } = get();
        if (!currentSession) return;
        try {
          await sessionsApi.stop(currentSession.id);
          set({
            currentSession: null,
            isActive: false,
            elapsedSeconds: 0
          });
          // Refresh stats
          useStatsStore.getState().fetchTodayStats();
          useStatsStore.getState().fetchDashboardStats();
        } catch (error) {
          console.error('Failed to stop session', error);
        }
      },

      tick: () => {
        const { isActive } = get();
        if (isActive) {
          set((state) => ({ elapsedSeconds: state.elapsedSeconds + 1 }));
        }
      }
    }),
    {
      name: 'session-storage',
      partialize: (state) => ({
        selectedTaskId: state.selectedTaskId,
        currentSession: state.currentSession,
        elapsedSeconds: state.elapsedSeconds,
        isActive: state.isActive
      }),
    }
  )
);
