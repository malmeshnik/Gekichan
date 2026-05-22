import { Clock, Calendar } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import type { Task } from "@/entities/task/taskStore";
import { cn } from "@/shared/lib/cn";
import { formatFocusTime } from "@/shared/lib/format/time";

interface TaskCardProps {
  task: Task;
  onClick?: () => void;
  onToggleStatus?: (e: React.MouseEvent) => void;
}

export function TaskCard({ task, onClick }: TaskCardProps) {
  const isDone = task.status === "done";

  const urgency = (() => {
    if (isDone || !task.deadline) return "normal";
    const deadlineDate = new Date(task.deadline);
    const now = new Date();
    const diffMs = deadlineDate.getTime() - now.getTime();

    if (diffMs < 0) return "overdue"; // Red
    if (diffMs < 3600000) return "warning"; // Orange (< 1 hour)
    return "normal";
  })();

  return (
    <SurfacePanel
      variant="glass"
      className={cn(
        "group relative flex flex-col gap-3 p-4 transition-all duration-300 hover:border-primary/30 active:scale-[0.98] cursor-pointer",
        isDone && "opacity-60",
        urgency === "overdue" && "border-danger/40 bg-danger/5 shadow-[0_0_15px_rgba(255,59,48,0.1)]",
        urgency === "warning" && "border-orange-500/40 bg-orange-500/5 shadow-[0_0_15px_rgba(249,115,22,0.1)]"
      )}
      onClick={onClick}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 w-full">
          <div className="flex flex-col gap-0.5 overflow-hidden">
            <h3 className={cn(
                "typography-body font-medium text-text-main line-clamp-2 transition-all",
                isDone && "line-through text-text-muted"
            )}>
              {task.title}
            </h3>
            <div className="flex items-center gap-2">
                <span className="typography-label text-[10px] uppercase text-primary/70 font-bold tracking-wider">
                    {task.project_name || "Особисте"}
                </span>
                {task.priority === "high" && (
                    <span className="h-1.5 w-1.5 rounded-full bg-danger shadow-[0_0_8px_rgba(255,59,48,0.5)]" />
                )}
            </div>
          </div>
        </div>

      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3 text-text-muted">
          <div className="flex items-center gap-1">
            <Clock size={12} className="text-secondary/70" />
            <span className="typography-label text-[11px] font-medium">
              {formatFocusTime(task.focus_time || 0)}
            </span>
          </div>

          {task.deadline && (
              <div className="flex items-center gap-1">
                <Calendar size={12} className={cn(
                    urgency === "overdue" ? "text-danger" : urgency === "warning" ? "text-orange-500" : "text-primary/60"
                )} />
                <span className={cn(
                    "typography-label text-[11px] font-medium",
                    urgency === "overdue" ? "text-danger" : urgency === "warning" ? "text-orange-500" : ""
                )}>
                    {new Date(task.deadline).toLocaleString('uk-UA', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
          )}
        </div>

        <div className="flex items-center gap-2">
            <div className={cn(
                "rounded-full px-2 py-0.5 text-[9px] font-bold uppercase tracking-wider",
                task.priority === "high" ? "bg-danger/10 text-danger" :
                task.priority === "medium" ? "bg-primary/10 text-primary" :
                "bg-surface-container-highest text-text-muted"
            )}>
                {task.priority === 'high' ? 'Високий' : task.priority === 'medium' ? 'Середній' : 'Низький'}
            </div>
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
