import React, { useEffect, useState } from 'react';
import { Header } from '@/shared/ui/Header';
import { TaskListWidget } from '@/widgets/TaskListWidget';
import { Plus, X, Calendar, AlignLeft } from 'lucide-react';
import { useTaskStore } from '@/entities/taskStore';
import { useI18n } from '@/shared/lib/i18n';
import { showToast } from '@/shared/ui/Toast';

export const TasksPage: React.FC = () => {
  const { tasks, fetchTasks, fetchProjects, projects, addTask, isLoading } = useTaskStore();
  const { t } = useI18n();
  const [showModal, setShowModal] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [description, setDescription] = useState('');
  const [deadline, setDeadline] = useState('');
  const [selectedProjectId, setSelectedProjectId] = useState('');

  useEffect(() => {
    fetchTasks();
    fetchProjects();
  }, []);

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle || !selectedProjectId) return;

    await addTask({
      title: newTaskTitle,
      project: selectedProjectId,
      description,
      deadline: deadline || undefined,
      status: 'todo'
    });

    setNewTaskTitle('');
    setDescription('');
    setDeadline('');
    setShowModal(false);
    showToast(t('taskCreated'), 'success');
  };

  const todoTasks = tasks.filter(t => t.status !== 'done');
  const doneTasks = tasks.filter(t => t.status === 'done');

  return (
    <div className="pb-32 min-h-screen">
      <Header title={t('myTasks')} />

      <main className="px-md flex flex-col gap-xl">
        {isLoading && tasks.length === 0 ? (
          <div className="flex flex-col gap-md">
            <div className="h-4 w-24 bg-card animate-pulse rounded" />
            {[1, 2, 3].map(i => <div key={i} className="h-16 w-full bg-card animate-pulse rounded-2xl" />)}
          </div>
        ) : (
          <>
            <TaskListWidget title={t('todo')} tasks={todoTasks} />
            <TaskListWidget title={t('completed')} tasks={doneTasks} />
          </>
        )}
      </main>

      <button
        onClick={() => setShowModal(true)}
        className="fixed right-6 bottom-28 w-14 h-14 bg-primary-start text-white rounded-full flex items-center justify-center shadow-2xl shadow-primary-start/40 active:scale-95 transition-transform z-40"
      >
        <Plus size={32} />
      </button>

      {showModal && (
        <div className="fixed inset-0 z-50 flex items-end justify-center sm:items-center p-md bg-background/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full max-w-lg bg-card border border-border rounded-t-3xl sm:rounded-3xl p-lg shadow-2xl animate-in slide-in-from-bottom duration-300">
            <div className="flex items-center justify-between mb-lg">
              <h3 className="text-xl font-bold">{t('newTask')}</h3>
              <button onClick={() => setShowModal(false)} className="p-2 hover:bg-white/5 rounded-full">
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleAddTask} className="flex flex-col gap-md max-h-[70vh] overflow-y-auto pr-2">
              <div>
                <label className="text-[10px] font-bold text-text-secondary uppercase tracking-widest block mb-2">{t('title')}</label>
                <input
                  autoFocus
                  type="text"
                  required
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  placeholder={t('whatNeedsDone')}
                  className="w-full p-md bg-background border border-border rounded-2xl text-text-primary focus:border-primary-start outline-none transition-colors"
                />
              </div>

              <div>
                <label className="text-[10px] font-bold text-text-secondary uppercase tracking-widest block mb-2">{t('project')}</label>
                <select
                  required
                  value={selectedProjectId}
                  onChange={(e) => setSelectedProjectId(e.target.value)}
                  className="w-full p-md bg-background border border-border rounded-2xl text-text-primary focus:border-primary-start outline-none transition-colors appearance-none"
                >
                  <option value="">{t('selectProject')}</option>
                  {projects.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2">
                   <AlignLeft size={14} className="text-text-secondary" />
                   <label className="text-[10px] font-bold text-text-secondary uppercase tracking-widest block">{t('description')}</label>
                </div>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder={t('enterDescription')}
                  className="w-full p-md bg-background border border-border rounded-2xl text-text-primary min-h-[80px] focus:border-primary-start outline-none transition-colors"
                />
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2">
                   <Calendar size={14} className="text-text-secondary" />
                   <label className="text-[10px] font-bold text-text-secondary uppercase tracking-widest block">{t('deadline')}</label>
                </div>
                <input
                  type="date"
                  value={deadline}
                  onChange={(e) => setDeadline(e.target.value)}
                  className="w-full p-md bg-background border border-border rounded-2xl text-text-primary focus:border-primary-start outline-none transition-colors"
                />
              </div>

              <button
                type="submit"
                disabled={!newTaskTitle || !selectedProjectId}
                className="w-full p-md bg-primary-start text-white rounded-2xl font-bold mt-md disabled:opacity-50 transition-all active:scale-95 shadow-lg shadow-primary-start/20"
              >
                {t('createTask')}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
