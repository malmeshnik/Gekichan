import React, { useEffect, useState } from 'react';
import { Header } from '../shared/ui/Header';
import { Card } from '../shared/ui/Card';
import { Folder, ChevronRight, Plus, X } from 'lucide-react';
import { useTaskStore } from '../entities/taskStore';
import { useI18n } from '../shared/lib/i18n';
import { showToast } from '../shared/ui/Toast';

export const ProjectsPage: React.FC = () => {
  const { projects, tasks, fetchProjects, fetchTasks, addProject, isLoading } = useTaskStore();
  const { t } = useI18n();
  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    fetchProjects();
    fetchTasks();
  }, []);

  const handleAddProject = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name) return;
    await addProject({ name, description });
    setName('');
    setDescription('');
    setShowModal(false);
    showToast(t('projectCreated'), 'success');
  };

  const getTaskCount = (projectId: string) => {
    return tasks.filter(t => t.project === projectId).length;
  };

  return (
    <div className="pb-32 min-h-screen">
      <Header title={t('projects')} />

      <main className="px-md flex flex-col gap-md">
        {isLoading && projects.length === 0 ? (
          [1, 2, 3].map(i => <div key={i} className="h-24 w-full bg-card animate-pulse rounded-2xl" />)
        ) : (
          projects.map(project => (
            <Card key={project.id} className="flex items-center justify-between py-md">
              <div className="flex items-center gap-md">
                <div className="p-3 bg-primary-start/10 rounded-xl text-primary-start">
                  <Folder size={24} />
                </div>
                <div>
                  <h4 className="text-sm font-bold">{project.name}</h4>
                  <p className="text-xs text-text-secondary truncate max-w-[200px]">{project.description || t('noDescription')}</p>
                  <p className="text-[10px] font-bold text-primary-start mt-1 uppercase">{getTaskCount(project.id)} {t('tasks')}</p>
                </div>
              </div>
              <ChevronRight size={20} className="text-border" />
            </Card>
          ))
        )}

        <button
          onClick={() => setShowModal(true)}
          className="flex items-center justify-center gap-2 p-md border-2 border-dashed border-border rounded-2xl text-text-secondary hover:text-text-primary transition-colors mt-md"
        >
          <Plus size={20} />
          <span className="text-sm font-bold uppercase tracking-widest">{t('newProject')}</span>
        </button>
      </main>

      {/* Simple Add Project Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-end justify-center sm:items-center p-md bg-background/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full max-w-lg bg-card border border-border rounded-t-3xl sm:rounded-3xl p-lg shadow-2xl animate-in slide-in-from-bottom duration-300">
            <div className="flex items-center justify-between mb-lg">
              <h3 className="text-xl font-bold">{t('newProject')}</h3>
              <button onClick={() => setShowModal(false)} className="p-2 hover:bg-white/5 rounded-full">
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleAddProject} className="flex flex-col gap-md">
              <div>
                <label className="text-[10px] font-bold text-text-secondary uppercase tracking-widest block mb-2">{t('projectName')}</label>
                <input
                  autoFocus
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder={t('egDesignSystem')}
                  className="w-full p-md bg-background border border-border rounded-2xl text-text-primary"
                />
              </div>

              <div>
                <label className="text-[10px] font-bold text-text-secondary uppercase tracking-widest block mb-2">{t('description')}</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder={t('enterDescription')}
                  className="w-full p-md bg-background border border-border rounded-2xl text-text-primary min-h-[100px]"
                />
              </div>

              <button
                type="submit"
                disabled={!name}
                className="w-full p-md bg-primary-start text-white rounded-2xl font-bold mt-md disabled:opacity-50 transition-opacity"
              >
                {t('createProject')}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
