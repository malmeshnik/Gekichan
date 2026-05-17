import { LayoutGrid, Brush, Code, Plus } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";

export function HomeDayGrid() {
  return (
    <section className="stack-md">
      <h3 className="typography-headline-sm flex items-center gap-stack-sm">
        <LayoutGrid size={20} className="text-primary" />
        Будова Дня
      </h3>

      <div className="grid grid-cols-4 gap-gutter">
        <SurfacePanel className="aspect-square bg-primary/10 border-primary/30 flex items-center justify-center">
          <Brush size={20} className="text-primary" />
        </SurfacePanel>
        <SurfacePanel className="aspect-square bg-primary/10 border-primary/30 flex items-center justify-center">
          <Brush size={20} className="text-primary" />
        </SurfacePanel>
        <SurfacePanel className="aspect-square bg-secondary/10 border-secondary/30 flex items-center justify-center">
          <Code size={20} className="text-secondary" />
        </SurfacePanel>
        <SurfacePanel
          className="aspect-square border-dashed border-outline/50 flex items-center justify-center interactive"
          interactive
        >
          <Plus size={20} className="text-text-muted" />
        </SurfacePanel>
      </div>

      <p className="typography-label text-text-muted text-right">
        2 блоки дизайну, 1 блок коду
      </p>
    </section>
  );
}
