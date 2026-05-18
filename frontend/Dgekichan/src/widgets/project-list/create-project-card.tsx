import { Plus } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";

interface CreateProjectCardProps {
  onClick?: () => void;
}

export function CreateProjectCard({ onClick }: CreateProjectCardProps) {
  return (
    <SurfacePanel
      variant="glass"
      className="group flex flex-col items-center justify-center gap-3 border-dashed border-outline/40 py-8 transition-all hover:border-primary/50 hover:bg-primary/5 active:scale-[0.98]"
      onClick={onClick}
    >
      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-surface-container-highest transition-colors group-hover:bg-primary/20">
        <Plus className="text-text-muted transition-colors group-hover:text-primary" size={24} />
      </div>
      <span className="typography-headline-sm text-text-muted transition-colors group-hover:text-text-main">
        Створити проект
      </span>
    </SurfacePanel>
  );
}
