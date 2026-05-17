import { motion } from "framer-motion";
import { type ReactNode } from "react";
import { cn } from "@/shared/lib/cn";

interface BottomDockProps {
  children: ReactNode;
  className?: string;
}

export function BottomDock({ children, className }: BottomDockProps) {
  return (
    <div className="fixed bottom-8 left-0 right-0 z-50 flex justify-center px-4">
      <nav
        className={cn(
          "h-16 px-1.5 surface-matte-glass radius-full",
          "border border-white/5",
          "flex justify-between items-center w-full max-w-sm",
          "shadow-[0_8px_32px_rgba(0,0,0,0.6)]",
          className
        )}
      >
        {children}
      </nav>
    </div>
  );
}

interface BottomDockItemProps {
  icon: ReactNode;
  label: string;
  active?: boolean;
  onClick?: () => void;
}

export function BottomDockItem({ icon, label, active, onClick }: BottomDockItemProps) {
  return (
    <motion.button
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={cn(
        "flex flex-col items-center justify-center flex-1 h-[52px] relative radius-full transition-all duration-300",
        active ? "text-text-main" : "text-text-muted hover:text-text-main"
      )}
    >
      {active && (
        <motion.div
          layoutId="active-pill"
          className="absolute inset-1.5 bg-white/5 radius-full border border-white/5 shadow-inner"
          transition={{ type: "spring", bounce: 0.1, duration: 0.6 }}
        />
      )}

      <div className="relative z-10 flex flex-col items-center">
        <div className={cn(
          "transition-all duration-500",
          active ? "scale-100 text-primary" : "scale-90 opacity-40"
        )}>
          {icon}
        </div>
        <span className={cn(
          "text-[9px] font-medium tracking-wide mt-0.5 transition-opacity duration-500",
          active ? "opacity-80" : "opacity-0 h-0 overflow-hidden"
        )}>
          {label}
        </span>
      </div>
    </motion.button>
  );
}
