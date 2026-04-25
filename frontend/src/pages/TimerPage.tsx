import React, { useEffect, useRef, useState } from 'react';
import { Header } from '@/shared/ui/Header';
import { ProgressRing } from '@/shared/ui/ProgressRing';
import { TimerDisplay } from '@/shared/ui/TimerDisplay';
import { TimerControls } from '@/features/timer/TimerControls';
import { Badge } from '@/shared/ui/Badge';
import { Flame, CheckCircle2 } from 'lucide-react';
import { useSessionStore } from '@/entities/sessionStore';
import { useTaskStore } from '@/entities/taskStore';
import { useI18n } from '@/shared/lib/i18n';

export const TimerPage: React.FC = () => {
  const {
    elapsedSeconds,
    isActive,
    tick,
    startSession,
    pauseSession,
    stopSession,
    fetchActiveSession,
    selectedTaskId,
    setSelectedTaskId
  } = useSessionStore();

  const { tasks, fetchTasks } = useTaskStore();
  const { t } = useI18n();
  const [showTaskSelector, setShowTaskSelector] = useState(false);

  useEffect(() => {
    fetchActiveSession();
    fetchTasks();
  }, []);

  useEffect(() => {
    let interval: number;
    if (isActive) {
      interval = window.setInterval(() => {
        tick();
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isActive, tick]);

  const selectedTask = tasks.find(t => t.id === selectedTaskId);
  const visualTargetSeconds = 25 * 60;
  const progress = Math.min(100, (elapsedSeconds / visualTargetSeconds) * 100);

  return (
    <div className="pb-32 min-h-screen flex flex-col">
      <Header title={t('focusTimer')} />

      <main className="flex-1 flex flex-col items-center justify-around px-md py-lg">
        {/* Indicators */}
        <div className="flex gap-md w-full max-w-xs">
          <div className="flex-1 bg-card border border-border rounded-2xl p-3 flex items-center justify-center gap-2">
            <Flame size={16} className="text-orange-500" />
            <span className="text-[10px] font-bold uppercase tracking-widest">{t('activeSession')}</span>
          </div>
        </div>

        {/* Current Task */}
        <div className="text-center w-full max-w-xs relative">
          <p className="text-[10px] font-bold text-text-secondary uppercase tracking-[0.2em] mb-2">{t('currentTask')}</p>
          <div
            onClick={() => !isActive && setShowTaskSelector(!showTaskSelector)}
            className={`cursor-pointer p-2 rounded-xl transition-colors ${!isActive ? 'hover:bg-card border border-transparent hover:border-border' : ''}`}
          >
            <h2 className="text-xl font-bold mb-1 truncate">
              {selectedTask ? selectedTask.title : t('noTaskSelected')}
            </h2>
            {selectedTask && <Badge variant="primary">{t('project')}: {selectedTask.project.slice(0, 8)}</Badge>}
            {!selectedTask && !isActive && <span className="text-xs text-primary-start">{t('tapToSelectTask')}</span>}
          </div>

          {showTaskSelector && !isActive && (
            <div className="absolute z-10 left-1/2 -translate-x-1/2 bottom-full mb-2 w-64 bg-card border border-border rounded-2xl shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
              <div className="max-h-60 overflow-y-auto">
                <div
                  className="p-3 hover:bg-white/5 border-b border-border flex items-center justify-between"
                  onClick={() => { setSelectedTaskId(null); setShowTaskSelector(false); }}
                >
                  <span className="text-sm">{t('noTask')}</span>
                  {!selectedTaskId && <CheckCircle2 size={16} className="text-primary-start" />}
                </div>
                {tasks.map(task => (
                  <div
                    key={task.id}
                    className="p-3 hover:bg-white/5 border-b border-border flex items-center justify-between"
                    onClick={() => { setSelectedTaskId(task.id); setShowTaskSelector(false); }}
                  >
                    <span className="text-sm truncate mr-2">{task.title}</span>
                    {selectedTaskId === task.id && <CheckCircle2 size={16} className="text-primary-start" />}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Timer Ring */}
        <div className="relative my-lg">
           <div className="absolute inset-0 bg-primary-start/5 blur-[100px] rounded-full" />
           <ProgressRing progress={progress}>
             <TimerDisplay seconds={elapsedSeconds} label={t('elapsed')} />
           </ProgressRing>
        </div>

        {/* Controls */}
        <TimerControls
          isActive={isActive}
          onStart={() => startSession()}
          onPause={() => pauseSession()}
          onStop={() => stopSession()}
          onAdjust={() => {}}
        />

        <p className="text-[10px] text-text-secondary uppercase tracking-widest mt-lg text-center px-lg">
          {isActive ? t('logInterruption') : ''}
        </p>
      </main>
    </div>
  );
};
