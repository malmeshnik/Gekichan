import { MoreHorizontal, ListTodo, Clock } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import type { Project } from "@/entities/project/projectStore";
import { cn } from "@/shared/lib/cn";
import { formatFocusTime } from "@/shared/lib/format/time";

interface ProjectCardProps {
  project: Project;
  onClick?: () => void;
  onAction?: (e: React.MouseEvent) => void;
}

export function ProjectCard({ project, onClick, onAction }: ProjectCardProps) {
  const progress = project.tasks_count > 0
    ? Math.round((project.done_tasks_count / project.tasks_count) * 100)
    : 0;

  const accentColors = [
    "bg-primary",
    "bg-secondary",
    "bg-accent-blue",
    "bg-accent-purple",
    "bg-accent-emerald",
    "bg-danger"
  ];
  const accentColor = accentColors[project.id % accentColors.length];

  return (
    <SurfacePanel
      variant="glass"
      className="group relative flex flex-col gap-4 p-5 transition-all duration-300 hover:border-primary/30 active:scale-[0.98] cursor-pointer"
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-start justify-between">
        <div className="flex flex-col gap-1">
          <h3 className="typography-headline-sm text-text-main line-clamp-1">
            {project.name}
          </h3>
          <p className="typography-body-sm text-text-muted line-clamp-2 min-h-[2.5rem]">
            {project.description || "Немає опису"}
          </p>
        </div>
      </div>

      {/* Progress & Time */}
      <div className="flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-text-muted">
            <Clock size={14} className="text-secondary" />
            <span className="typography-label text-[12px]">
              {formatFocusTime(project.total_focus_time || 0)}
            </span>
          </div>
          <span className="typography-label text-primary">{progress}%</span>
        </div>

        {/* Progress Bar */}
        <div className="h-1.5 w-full overflow-hidden rounded-full bg-surface-container-highest">
          <div
            className="h-full bg-gradient-to-r from-primary to-secondary transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between pt-1">
        <div className="flex -space-x-2">
          {[...Array(Math.min(project.members_count, 3))].map((_, i) => (
            <div
              key={i}
              className="h-6 w-6 rounded-full border-2 border-surface-container-high bg-surface-container-highest overflow-hidden"
            >
               <img
                src={`https://api.dicebear.com/7.x/avataaars/svg?seed=ProjectMember${i}${project.id}`}
                alt="member"
              />
            </div>
          ))}
          {project.members_count > 3 && (
            <div className="flex h-6 w-6 items-center justify-center rounded-full border-2 border-surface-container-high bg-surface-container-highest text-[10px] text-text-muted">
              +{project.members_count - 3}
            </div>
          )}
        </div>

        <div className="flex items-center gap-1.5 text-text-muted">
          <ListTodo size={14} />
          <span className="typography-label text-[12px]">
            {project.done_tasks_count}/{project.tasks_count}
          </span>
        </div>
      </div>

      {/* Left accent border */}
      <div
        className={cn(
          "absolute left-0 top-1/4 h-1/2 w-1 rounded-r-full",
          progress === 100 ? "bg-secondary" : accentColor
        )}
      />
    </SurfacePanel>
  );
}
