import React from 'react';
import { Header } from '../shared/ui/Header';
import { Card } from '../shared/ui/Card';
import { Button } from '../shared/ui/Button';
import { StatsGrid } from '../widgets/StatsGrid';
import { TaskListWidget } from '../widgets/TaskListWidget';
import { Play, Plus, Lightbulb } from 'lucide-react';
import { useTaskStore } from '../entities/model';
import { useEffect } from 'react';

export const DashboardPage: React.FC = () => {
  const { tasks, setTasks } = useTaskStore();

  useEffect(() => {
    if (tasks.length === 0) {
      setTasks([
        { id: '1', title: 'Finalize Q3 Report', status: 'todo', project: 'p1', deadline: '2024-04-24T10:00:00Z' },
        { id: '2', title: 'Client Feedback Call', status: 'todo', project: 'p2', deadline: '2024-04-24T14:30:00Z' },
        { id: '3', title: 'Review Design Assets', status: 'todo', project: 'p1', deadline: '2024-04-24T16:00:00Z' },
      ]);
    }
  }, []);

  const nextTasks = tasks.slice(0, 3);

  return (
    <div className="pb-32">
      <Header title="Productivity" />

      <main className="px-md flex flex-col gap-lg">
        {/* Greeting & Score */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-md">
            <div className="w-16 h-16 rounded-full border-4 border-primary-start flex items-center justify-center text-xl font-bold">
              85
            </div>
            <div>
              <p className="text-text-secondary text-sm">Good Morning,</p>
              <h2 className="text-xl font-bold">Alex</h2>
            </div>
          </div>
          <div className="text-right">
            <p className="text-[10px] font-bold text-primary-start uppercase tracking-wider">Today's Focus</p>
            <p className="text-lg font-bold">4.5h</p>
            <p className="text-xs text-green-500 font-medium">~ +15% vs yesterday</p>
          </div>
        </div>

        {/* Daily Insight */}
        <Card className="bg-gradient-to-br from-card to-card/50 border-primary-start/20">
          <div className="flex gap-md">
            <div className="p-2 bg-orange-500/10 rounded-lg h-fit">
              <Lightbulb className="text-orange-500" size={20} />
            </div>
            <div>
              <h4 className="text-sm font-bold mb-1">Daily Insight</h4>
              <p className="text-xs text-text-secondary leading-relaxed">
                You've hit your focus goals 4 days in a row! Tackle your hardest task first today to keep the momentum going.
              </p>
            </div>
          </div>
        </Card>

        {/* Quick Actions */}
        <div className="flex flex-col gap-sm">
          <Button fullWidth className="gap-2 py-4">
            <Play size={18} fill="currentColor" /> Start Focus Session
          </Button>
          <Button variant="secondary" fullWidth className="gap-2 border-dashed border-2 border-border py-4">
            <Plus size={18} /> Quick Add Task
          </Button>
        </div>

        {/* Stats Grid */}
        <StatsGrid />

        {/* Next Up Tasks */}
        <TaskListWidget title="Next Up" tasks={nextTasks} onSeeAll={() => {}} />
      </main>
    </div>
  );
};
