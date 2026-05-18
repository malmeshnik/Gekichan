import { useEffect, useMemo, useState } from "react";
import { useTaskStore } from "@/entities/task/taskStore";
import { useProjectStore } from "@/entities/project/projectStore";
import { TaskCard } from "./task-card";
import { Plus, LayoutGrid } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { CreateTaskModal } from "./create-task-modal";

interface TaskListProps {
  projectId?: number | null;
}

export function TaskList({ projectId }: TaskListProps) {
  const { tasks, fetchTasks, isLoading } = useTaskStore();
  const { projects, fetchProjects } = useProjectStore();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  useEffect(() => {
    fetchTasks();
    if (projects.length === 0) fetchProjects();
  }, [fetchTasks, fetchProjects, projects.length]);

  const currentProject = useMemo(() =>
    projectId ? projects.find(p => p.id === projectId) : null
  , [projectId, projects]);

  const filteredTasks = useMemo(() => {
    if (!projectId) return tasks;
    return tasks.filter(t => t.project_name === currentProject?.name);
  }, [tasks, projectId, currentProject]);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between px-2">
        <div className="flex flex-col">
            <h1 className="typography-headline-lg">
                {projectId ? "Завдання проєкту" : "Всі завдання"}
            </h1>
            {currentProject && (
                <span className="typography-label text-primary">{currentProject.name}</span>
            )}
        </div>

        <button
            className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-background shadow-lg shadow-primary/20 transition-transform active:scale-90"
            onClick={() => setIsCreateModalOpen(true)}
        >
          <Plus size={24} />
        </button>
      </div>

      <div className="flex flex-col gap-3 pb-24">
        {isLoading ? (
          <div className="flex justify-center py-10 text-text-muted">Завантаження...</div>
        ) : filteredTasks.length > 0 ? (
          filteredTasks.map((task) => (
            <TaskCard key={task.id} task={task} />
          ))
        ) : (
          <SurfacePanel variant="glass" className="flex flex-col items-center justify-center py-12 text-center text-text-muted">
            <LayoutGrid size={40} className="mb-4 opacity-20" />
            <p>Завдань не знайдено</p>
          </SurfacePanel>
        )}
      </div>

      <CreateTaskModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        initialProjectId={projectId}
      />
    </div>
  );
}
