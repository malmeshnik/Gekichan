import React from 'react';
import { Header } from '../shared/ui/Header';
import { Card } from '../shared/ui/Card';
import { Folder, ChevronRight, Plus } from 'lucide-react';

const mockProjects = [
  { id: '1', name: 'Design System', description: 'Internal branding & UI kit', taskCount: 12 },
  { id: '2', name: 'Q3 Marketing', description: 'Campaign for new release', taskCount: 8 },
  { id: '3', name: 'Admin & Setup', description: 'Operations & infrastructure', taskCount: 6 },
];

export const ProjectsPage: React.FC = () => {
  return (
    <div className="pb-32 min-h-screen">
      <Header title="Projects" />

      <main className="px-md flex flex-col gap-md">
        {mockProjects.map(project => (
          <Card key={project.id} className="flex items-center justify-between py-md">
            <div className="flex items-center gap-md">
              <div className="p-3 bg-primary-start/10 rounded-xl text-primary-start">
                <Folder size={24} />
              </div>
              <div>
                <h4 className="text-sm font-bold">{project.name}</h4>
                <p className="text-xs text-text-secondary truncate max-w-[200px]">{project.description}</p>
                <p className="text-[10px] font-bold text-primary-start mt-1 uppercase">{project.taskCount} Tasks</p>
              </div>
            </div>
            <ChevronRight size={20} className="text-border" />
          </Card>
        ))}

        <button className="flex items-center justify-center gap-2 p-md border-2 border-dashed border-border rounded-2xl text-text-secondary hover:text-text-primary transition-colors mt-md">
          <Plus size={20} />
          <span className="text-sm font-bold uppercase tracking-widest">Create New Project</span>
        </button>
      </main>
    </div>
  );
};
