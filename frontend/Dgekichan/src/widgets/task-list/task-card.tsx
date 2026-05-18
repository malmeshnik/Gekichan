import { MoreHorizontal, Clock, CheckCircle2, Circle } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { Task } from "@/entities/task/taskStore";
import { cn } from "@/shared/lib/cn";
import { formatFocusTime } from "@/shared/lib/format/time";

interface TaskCardProps {
  task: Task & { focus_time?: number };
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
        <div className="flex items-start gap-3">
          <button
            className="mt-1 text-text-muted hover:text-primary transition-colors"
            onClick={(e) => {
                e.stopPropagation();
                onToggleStatus?.(e);
            }}
          >
            {isDone ? (
                <CheckCircle2 size={20} className="text-secondary" />
            ) : (
                <Circle size={20} />
            )}
          </button>

          <div className="flex flex-col gap-0.5">
            <h3 className={cn(
                "typography-body font-medium text-text-main line-clamp-2",
                isDone && "line-through"
            )}>
              {task.title}
            </h3>
            {task.project_name && (
                <span className="typography-label text-[10px] uppercase text-primary/70">
                    {task.project_name}
                </span>
            )}
          </div>
        </div>

        <button className="p-1 text-text-muted hover:text-text-main transition-colors">
          <MoreHorizontal size={18} />
        </button>
      </div>

      <div className="flex items-center justify-between pl-8">
        <div className="flex items-center gap-1.5 text-text-muted">
          <Clock size={12} className="text-secondary/70" />
          <span className="typography-label text-[11px]">
            {formatFocusTime(task.focus_time || 0)}
          </span>
        </div>

        {task.priority !== "medium" && (
            <div className={cn(
                "rounded-full px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider",
                task.priority === "high" ? "bg-danger/10 text-danger" : "bg-surface-container-highest text-text-muted"
            )}>
                {task.priority}
            </div>
        )}
      </div>
    </SurfacePanel>
  );
}
