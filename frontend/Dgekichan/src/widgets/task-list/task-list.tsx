import { useEffect, useMemo, useState } from "react";
import { useTaskStore } from "@/entities/task/taskStore";
import type { Task } from "@/entities/task/taskStore";
import { useProjectStore } from "@/entities/project/projectStore";
import { TaskCard } from "./task-card";
import { Plus, LayoutGrid } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { CreateTaskModal } from "./create-task-modal";
import { EditTaskModal } from "./edit-task-modal";
import { cn } from "@/shared/lib/cn";

interface TaskListProps {
  projectId?: number | null;
}

export function TaskList({ projectId }: TaskListProps) {
  const { tasks, fetchTasks, updateTask, isLoading } = useTaskStore();
  const { projects, fetchProjects } = useProjectStore();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [activeFilter, setActiveFilter] = useState<"all" | "today" | "week" | "month">("all");

  useEffect(() => {
    const params: any = projectId ? { project: projectId } : {};
    if (activeFilter !== "all") {
        params.period = activeFilter;
    }
    fetchTasks(params);
    if (projects.length === 0) fetchProjects();
  }, [fetchTasks, fetchProjects, projectId, projects.length, activeFilter]);

  const currentProject = useMemo(() =>
    projectId ? projects.find(p => p.id === projectId) : null
  , [projectId, projects]);

  const sortedTasks = useMemo(() => {
      return [...tasks].sort((a, b) => {
          // Status priority: todo/in_progress first, done last
          if (a.status === "done" && b.status !== "done") return 1;
          if (a.status !== "done" && b.status === "done") return -1;

          // If both are not done
          if (a.status !== "done" && b.status !== "done") {
              // 1. Sort by priority
              const prioWeight = { high: 3, medium: 2, low: 1 };
              if (prioWeight[b.priority] !== prioWeight[a.priority]) {
                  return prioWeight[b.priority] - prioWeight[a.priority];
              }

              // 2. Sort by deadline (nearest first)
              if (a.deadline && b.deadline) {
                  return new Date(a.deadline).getTime() - new Date(b.deadline).getTime();
              }
              if (a.deadline) return -1;
              if (b.deadline) return 1;
          }

          return 0;
      });
  }, [tasks]);

  const handleToggleStatus = async (task: any) => {
      const newStatus = task.status === "done" ? "todo" : "done";
      await updateTask(task.id, { status: newStatus });
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between px-2">
        <div className="flex flex-col">
            <h1 className="typography-headline-lg">
                {currentProject ? `Завдання: ${currentProject.name}` : "Всі завдання"}
            </h1>
            {currentProject && (
                <span className="typography-label text-primary uppercase tracking-widest text-[10px]">ПРОЄКТ</span>
            )}
        </div>

        <button
            className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-background shadow-lg shadow-primary/20 transition-transform active:scale-90"
            onClick={() => setIsCreateModalOpen(true)}
        >
          <Plus size={24} />
        </button>
      </div>

      {/* Filters */}
      <div className="flex overflow-x-auto gap-2 px-2 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:'none'] [scrollbar-width:'none']">
        {[
          { id: "all", label: "Усі" },
          { id: "today", label: "На сьогодні" },
          { id: "week", label: "На тиждень" },
          { id: "month", label: "На місяць" },
        ].map((filter) => (
          <button
            key={filter.id}
            onClick={() => setActiveFilter(filter.id as any)}
            className={cn(
              "px-4 py-2 rounded-full typography-label whitespace-nowrap transition-all border",
              activeFilter === filter.id
                ? "bg-primary text-background border-primary"
                : "bg-surface-container-low text-text-muted border-outline/10 hover:border-outline/30"
            )}
          >
            {filter.label}
          </button>
        ))}
      </div>

      <div className="flex flex-col gap-3 pb-24">
        {isLoading ? (
          <div className="flex justify-center py-10 text-text-muted">Завантаження...</div>
        ) : sortedTasks.length > 0 ? (
          sortedTasks.map((task) => (
            <TaskCard
                key={task.id}
                task={task}
                onToggleStatus={() => handleToggleStatus(task)}
                onClick={() => setSelectedTask(task)}
            />
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

      {selectedTask && (
          <EditTaskModal
            isOpen={!!selectedTask}
            onClose={() => setSelectedTask(null)}
            task={selectedTask}
          />
      )}
    </div>
  );
}
