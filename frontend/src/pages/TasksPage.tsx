import React from 'react';
import { Header } from '../shared/ui/Header';
import { TaskListWidget } from '../widgets/TaskListWidget';
import { Plus } from 'lucide-react';
import { useTaskStore } from '../entities/model';
import { useEffect } from 'react';

export const TasksPage: React.FC = () => {
  const { tasks, setTasks } = useTaskStore();

  useEffect(() => {
    if (tasks.length === 0) {
      setTasks([
        { id: '1', title: 'Finalize Q3 OKRs', status: 'todo', project_name: 'Strategy 60%', deadline: '2024-04-24T09:00:00Z', project: 'p1' },
        { id: '2', title: 'Design System Review', status: 'todo', project_name: 'Design 85%', deadline: '2024-04-24T11:00:00Z', project: 'p1' },
        { id: '3', title: 'Client Kickoff Call', status: 'done', project_name: 'Meetings 100%', deadline: '2024-04-24T14:00:00Z', project: 'p1' },
        { id: '4', title: 'Update Marketing Assets', status: 'todo', project_name: 'Marketing 20%', deadline: '2024-04-25T10:00:00Z', project: 'p1' },
        { id: '5', title: 'Weekly Sync Preparation', status: 'todo', project_name: 'Internal 0%', deadline: '2024-04-25T15:00:00Z', project: 'p1' },
      ]);
    }
  }, []);

  const todayTasks = tasks.filter(t => new Date(t.deadline || '').toDateString() === new Date('2024-04-24').toDateString());
  const upcomingTasks = tasks.filter(t => new Date(t.deadline || '').toDateString() !== new Date('2024-04-24').toDateString());

  return (
    <div className="pb-32 min-h-screen">
      <Header title="Productivity" />

      <main className="px-md flex flex-col gap-xl">
        <TaskListWidget title="Today" tasks={todayTasks} />
        <TaskListWidget title="Upcoming" tasks={upcomingTasks} />
      </main>

      {/* Floating Action Button */}
      <button className="fixed right-6 bottom-28 w-14 h-14 bg-primary-start text-white rounded-full flex items-center justify-center shadow-2xl shadow-primary-start/40 active:scale-95 transition-transform z-40">
        <Plus size={32} />
      </button>
    </div>
  );
};
