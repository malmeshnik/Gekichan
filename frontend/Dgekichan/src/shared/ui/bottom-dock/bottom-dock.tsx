import { motion } from "framer-motion";
import { type ReactNode } from "react";
import { cn } from "@/shared/lib/cn";
import { surfacePanelVariants } from "@/shared/ui/surface-panel/surface-panel.variants";

interface BottomDockProps {
  children: ReactNode;
  className?: string;
}

export function BottomDock({ children, className }: BottomDockProps) {
  return (
    <nav
      className={cn(
        surfacePanelVariants({ variant: "glass-heavy" }),
        "fixed bottom-0 left-0 right-0 z-50",
        "h-20 px-stack-lg pb-safe",
        "border-t border-white/5",
        "flex justify-around items-center !rounded-none",
        "shadow-[0_-8px_32px_rgba(0,0,0,0.4)]",
        className
      )}
    >
      {children}
    </nav>
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
      whileTap={{ scale: 0.9 }}
      onClick={onClick}
      className={cn(
        "flex flex-col items-center justify-center stack-sm min-w-16 h-full relative",
        "transition-colors duration-300",
        active ? "text-primary" : "text-text-muted hover:text-text-main"
      )}
    >
      <div className={cn(
        "p-stack-sm radius-panel transition-standard",
        active && "bg-primary/10 glow-primary"
      )}>
        {icon}
      </div>
      <span className="typography-label lowercase text-[10px]">{label}</span>

      {active && (
        <motion.div
          layoutId="active-nav"
          className="absolute -top-1 w-1 h-1 bg-primary rounded-full shadow-[0_0_8px_var(--primary)]"
        />
      )}
    </motion.button>
  );
}
