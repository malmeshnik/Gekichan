import { MoreHorizontal, Clock, CheckCircle2, Circle } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import type { Task } from "@/entities/task/taskStore";
import { cn } from "@/shared/lib/cn";
import { formatFocusTime } from "@/shared/lib/format/time";

interface TaskCardProps {
  task: Task;
  onClick?: () => void;
  onToggleStatus?: (e: React.MouseEvent) => void;
}

export function TaskCard({ task, onClick, onToggleStatus }: TaskCardProps) {
  const isDone = task.status === "done";

  return (
    <SurfacePanel
      variant="glass"
      className={cn(
        "group relative flex flex-col gap-3 p-4 transition-all duration-300 hover:border-primary/30 active:scale-[0.98] cursor-pointer",
        isDone && "opacity-60"
      )}
      onClick={onClick}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 w-full">
          <button
            className="mt-1 shrink-0 text-text-muted hover:text-primary transition-colors"
            onClick={(e) => {
                e.stopPropagation();
                onToggleStatus?.(e);
            }}
          >
            {isDone ? (
                <CheckCircle2 size={24} className="text-secondary" />
            ) : (
                <Circle size={24} />
            )}
          </button>

          <div className="flex flex-col gap-0.5 overflow-hidden">
            <h3 className={cn(
                "typography-body font-medium text-text-main line-clamp-2 transition-all",
                isDone && "line-through text-text-muted"
            )}>
              {task.title}
            </h3>
            <div className="flex items-center gap-2">
                {task.project_name && (
                    <span className="typography-label text-[10px] uppercase text-primary/70 font-bold tracking-wider">
                        {task.project_name}
                    </span>
                )}
                {task.priority === "high" && (
                    <span className="h-1.5 w-1.5 rounded-full bg-danger shadow-[0_0_8px_rgba(255,59,48,0.5)]" />
                )}
            </div>
          </div>
        </div>

        <button
            className="p-1 text-text-muted hover:text-text-main transition-colors shrink-0"
            onClick={(e) => {
                e.stopPropagation();
                // Task action menu could be here
            }}
        >
          <MoreHorizontal size={18} />
        </button>
      </div>

      <div className="flex items-center justify-between pl-9">
        <div className="flex items-center gap-1.5 text-text-muted">
          <Clock size={12} className="text-secondary/70" />
          <span className="typography-label text-[11px] font-medium">
            {formatFocusTime(task.focus_time || 0)}
          </span>
        </div>

        <div className="flex items-center gap-2">
            {task.priority !== "medium" && (
                <div className={cn(
                    "rounded-full px-2 py-0.5 text-[9px] font-bold uppercase tracking-wider",
                    task.priority === "high" ? "bg-danger/10 text-danger" : "bg-surface-container-highest text-text-muted"
                )}>
                    {task.priority}
                </div>
            )}
            <span className={cn(
                "text-[9px] font-bold uppercase px-2 py-0.5 rounded-full",
                isDone ? "bg-secondary/10 text-secondary" : "bg-primary/10 text-primary"
            )}>
                {task.status === "todo" ? "Треба зробити" : task.status === "in_progress" ? "У процесі" : "Готово"}
            </span>
        </div>
      </div>
    </SurfacePanel>
  );
}
