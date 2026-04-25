import React, { useEffect } from 'react';
import { Header } from '@/shared/ui/Header';
import { Card } from '@/shared/ui/Card';
import { Button } from '@/shared/ui/Button';
import { StatsGrid } from '@/widgets/StatsGrid';
import { TaskListWidget } from '@/widgets/TaskListWidget';
import { Play, Plus, Lightbulb } from 'lucide-react';
import { useTaskStore } from '@/entities/taskStore';
import { useStatsStore } from '@/entities/statsStore';
import { useAuthStore } from '@/entities/authStore';
import { useI18n } from '@/shared/lib/i18n';
import { useNavigate } from 'react-router-dom';

export const DashboardPage: React.FC = () => {
  const { tasks, fetchTasks, isLoading: tasksLoading } = useTaskStore();
  const { today, fetchTodayStats, isLoading: statsLoading } = useStatsStore();
  const { telegramId } = useAuthStore();
  const { t } = useI18n();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTasks();
    fetchTodayStats();
  }, []);

  const nextTasks = tasks.filter(t => t.status !== 'done').slice(0, 3);

  const formatFocusTime = (seconds: number) => {
    const hours = (seconds / 3600).toFixed(1);
    return `${hours}h`;
  };

  return (
    <div className="pb-32">
      <Header title={t('dashboard')} />

      <main className="px-md flex flex-col gap-lg">
        {/* Greeting & Score */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-md">
            <div className="w-16 h-16 rounded-full border-4 border-primary-start flex items-center justify-center text-xl font-bold">
              {statsLoading ? '...' : (today?.completed_tasks_count || 0) * 10}
            </div>
            <div>
              <p className="text-text-secondary text-sm">{t('welcomeBack')},</p>
              <h2 className="text-xl font-bold truncate max-w-[120px]">{t('user')} {telegramId}</h2>
            </div>
          </div>
          <div className="text-right">
            <p className="text-[10px] font-bold text-primary-start uppercase tracking-wider">{t('todayFocus')}</p>
            <p className="text-lg font-bold">{statsLoading ? '...' : formatFocusTime(today?.total_focus_time || 0)}</p>
          </div>
        </div>

        {/* Daily Insight */}
        <Card className="bg-gradient-to-br from-card to-card/50 border-primary-start/20">
          <div className="flex gap-md">
            <div className="p-2 bg-orange-500/10 rounded-lg h-fit">
              <Lightbulb className="text-orange-500" size={20} />
            </div>
            <div>
              <h4 className="text-sm font-bold mb-1">{t('dailyInsight')}</h4>
              <p className="text-xs text-text-secondary leading-relaxed">
                {t('insightContent').replace('{count}', nextTasks.length.toString())}
              </p>
            </div>
          </div>
        </Card>

        {/* Quick Actions */}
        <div className="flex flex-col gap-sm">
          <Button fullWidth className="gap-2 py-4" onClick={() => navigate('/timer')}>
            <Play size={18} fill="currentColor" /> {t('timer')}
          </Button>
          <Button variant="secondary" fullWidth className="gap-2 border-dashed border-2 border-border py-4" onClick={() => navigate('/tasks')}>
            <Plus size={18} /> {t('tasks')}
          </Button>
        </div>

        {/* Stats Grid */}
        <StatsGrid />

        {/* Next Up Tasks */}
        {tasksLoading ? (
           <div className="flex flex-col gap-md">
              <div className="h-4 w-24 bg-card animate-pulse rounded" />
              <div className="h-16 w-full bg-card animate-pulse rounded-2xl" />
              <div className="h-16 w-full bg-card animate-pulse rounded-2xl" />
           </div>
        ) : (
          <TaskListWidget title={t('nextUp')} tasks={nextTasks} onSeeAll={() => navigate('/tasks')} />
        )}
      </main>
    </div>
  );
};
