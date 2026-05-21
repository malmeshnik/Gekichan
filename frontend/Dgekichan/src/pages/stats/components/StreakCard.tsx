import { SurfacePanel } from "@/shared/ui/surface-panel/surface-panel";
import { Timer, CheckCircle2 } from "lucide-react";

interface StreakCardProps {
  type: "focus" | "tasks";
  count: number;
  label: string;
}

export function StreakCard({ type, count, label }: StreakCardProps) {
  const Icon = type === "focus" ? Timer : CheckCircle2;
  const accentColor = type === "focus" ? "text-primary" : "text-secondary";
  const borderColor = type === "focus" ? "border-l-primary" : "border-l-secondary";

  return (
    <SurfacePanel
        variant="elevated"
        className={`p-4 flex flex-col gap-6 border-l-2 ${borderColor} flex-1`}
    >
      <div className="flex justify-between items-start">
        <div className={`p-2 rounded-lg bg-white/5 ${accentColor}`}>
          <Icon size={20} />
        </div>
        <div className="opacity-20">
            <Icon size={40} />
        </div>
      </div>

      <div className="flex flex-col gap-1">
        <span className="text-3xl font-bold text-white">{count}</span>
        <span className="text-xs text-white/40 leading-tight">
          {label}
        </span>
      </div>
    </SurfacePanel>
  );
}
