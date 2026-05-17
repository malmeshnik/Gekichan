import { motion } from "framer-motion";
import { cn } from "@/shared/lib/cn";

interface StatBarProps {
  progress: number;
  label?: string;
  value?: string;
  variant?: "primary" | "danger" | "secondary";
  className?: string;
  showValueOnRight?: boolean;
}

export function StatBar({
  progress,
  label,
  value,
  variant = "primary",
  className,
}: StatBarProps) {
  return (
    <div className={cn("stack-sm w-full", className)}>
      {(label || value) && (
        <div className="flex justify-between items-center">
          {label && <span className="typography-body text-text-main">{label}</span>}
          {value && <span className={cn(
            "typography-label",
            variant === 'danger' ? "text-danger" : "text-primary"
          )}>
            {value}
          </span>}
        </div>
      )}
      <div className="h-3 w-full bg-surface-container-highest radius-full overflow-hidden">
        <motion.div
          className={cn(
            "h-full radius-full",
            variant === "primary" && "bg-primary",
            variant === "secondary" && "bg-secondary",
            variant === "danger" && "bg-danger"
          )}
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
      </div>
    </div>
  );
}
