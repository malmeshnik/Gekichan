import { motion } from "framer-motion";
import { cn } from "@/shared/lib/cn";

interface StatBarProps {
  progress: number;
  label?: string;
  value?: string;
  variant?: "primary" | "danger" | "secondary";
  className?: string;
}

export function StatBar({
  progress,
  label,
  value,
  variant = "primary",
  className,
}: StatBarProps) {
  const getGradient = () => {
    switch (variant) {
      case "primary": return "from-primary/60 to-primary/30";
      case "secondary": return "from-secondary/60 to-secondary/30";
      case "danger": return "from-danger/60 to-danger/30";
      default: return "from-primary/60 to-primary/30";
    }
  };

  return (
    <div className={cn("flex flex-col gap-2.5 w-full", className)}>
      <div className="h-1.5 w-full bg-black/20 radius-full overflow-hidden relative border border-white/5 shadow-inner">
        {/* Recessed track shadow */}
        <div className="absolute inset-0 shadow-[inset_0_1px_2px_rgba(0,0,0,0.4)] pointer-events-none" />

        <motion.div
          className={cn(
            "h-full radius-full bg-gradient-to-r relative",
            getGradient()
          )}
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 1.5, ease: [0.4, 0, 0.2, 1] }}
        />
      </div>

      {(label || value) && (
        <div className="flex justify-between items-center px-0.5">
          {label && <span className="text-[10px] font-medium text-text-muted uppercase tracking-wider">{label}</span>}
          {value && <span className={cn(
            "text-[10px] font-semibold tracking-tight",
            variant === 'danger' ? "text-danger/80" : "text-text-main/70"
          )}>
            {value}
          </span>}
        </div>
      )}
    </div>
  );
}
