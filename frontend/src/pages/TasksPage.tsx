import React, { useEffect, useState } from 'react';
import { Header } from '../shared/ui/Header';
import { TaskListWidget } from '../widgets/TaskListWidget';
import { Plus, X } from 'lucide-react';
import { useTaskStore } from '../entities/taskStore';

export const TasksPage: React.FC = () => {
  const { tasks, fetchTasks, fetchProjects, projects, addTask, isLoading } = useTaskStore();
  const [showModal, setShowModal] = useState(false);
  const [newTaskTitle, setNewTaskTitle] = useState('');
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
      status: 'todo'
    });

    setNewTaskTitle('');
    setShowModal(false);
  };

  const todoTasks = tasks.filter(t => t.status !== 'done');
  const doneTasks = tasks.filter(t => t.status === 'done');

  return (
    <div className="pb-32 min-h-screen">
      <Header title="My Tasks" />

      <main className="px-md flex flex-col gap-xl">
        {isLoading && tasks.length === 0 ? (
          <div className="flex flex-col gap-md">
            <div className="h-4 w-24 bg-card animate-pulse rounded" />
            {[1, 2, 3].map(i => <div key={i} className="h-16 w-full bg-card animate-pulse rounded-2xl" />)}
          </div>
        ) : (
          <>
            <TaskListWidget title="To Do" tasks={todoTasks} />
            <TaskListWidget title="Completed" tasks={doneTasks} />
          </>
        )}
      </main>

      {/* Floating Action Button */}
      <button
        onClick={() => setShowModal(true)}
        className="fixed right-6 bottom-28 w-14 h-14 bg-primary-start text-white rounded-full flex items-center justify-center shadow-2xl shadow-primary-start/40 active:scale-95 transition-transform z-40"
      >
        <Plus size={32} />
      </button>

      {/* Simple Add Task Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-end justify-center sm:items-center p-md bg-background/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full max-w-lg bg-card border border-border rounded-t-3xl sm:rounded-3xl p-lg shadow-2xl animate-in slide-in-from-bottom duration-300">
            <div className="flex items-center justify-between mb-lg">
              <h3 className="text-xl font-bold">New Task</h3>
              <button onClick={() => setShowModal(false)} className="p-2 hover:bg-white/5 rounded-full">
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleAddTask} className="flex flex-col gap-md">
              <div>
                <label className="text-[10px] font-bold text-text-secondary uppercase tracking-widest block mb-2">Title</label>
                <input
                  autoFocus
                  type="text"
                  value={newTaskTitle}
                  onChange={(e) => setNewTaskTitle(e.target.value)}
                  placeholder="What needs to be done?"
                  className="w-full p-md bg-background border border-border rounded-2xl text-text-primary"
                />
              </div>

              <div>
                <label className="text-[10px] font-bold text-text-secondary uppercase tracking-widest block mb-2">Project</label>
                <select
                  value={selectedProjectId}
                  onChange={(e) => setSelectedProjectId(e.target.value)}
                  className="w-full p-md bg-background border border-border rounded-2xl text-text-primary"
                >
                  <option value="">Select a project</option>
                  {projects.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>

              <button
                type="submit"
                disabled={!newTaskTitle || !selectedProjectId}
                className="w-full p-md bg-primary-start text-white rounded-2xl font-bold mt-md disabled:opacity-50 transition-opacity"
              >
                Create Task
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
