import { LayoutGrid, Brush, Code, Plus } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";

export function HomeDayGrid() {
  return (
    <section className="flex flex-col gap-5">
      <h3 className="typography-headline-sm flex items-center gap-2.5 text-text-main/90">
        <div className="p-2 bg-white/5 radius-xl border border-white/5 text-primary">
          <LayoutGrid size={16} />
        </div>
        Будова Дня
      </h3>

      <div className="grid grid-cols-4 gap-3">
        <SurfacePanel variant="default" className="aspect-square border-primary/20 radius-2xl flex items-center justify-center relative overflow-hidden group">
          <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity" />
          <Brush size={20} className="text-primary/70" />
        </SurfacePanel>
        <SurfacePanel variant="default" className="aspect-square border-primary/20 radius-2xl flex items-center justify-center relative overflow-hidden group">
          <div className="absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity" />
          <Brush size={20} className="text-primary/70" />
        </SurfacePanel>
        <SurfacePanel variant="default" className="aspect-square border-secondary/20 radius-2xl flex items-center justify-center relative overflow-hidden group">
          <div className="absolute inset-0 bg-secondary/5 opacity-0 group-hover:opacity-100 transition-opacity" />
          <Code size={20} className="text-secondary/70" />
        </SurfacePanel>
        <SurfacePanel
          variant="base"
          interactive
          className="aspect-square bg-white/5 border border-dashed border-white/10 radius-2xl flex items-center justify-center hover:bg-white/10 transition-colors group"
        >
          <Plus size={20} className="text-text-muted/50 group-hover:text-text-main transition-colors" />
        </SurfacePanel>
      </div>

      <p className="typography-label text-text-muted/60 text-right">
        2 блоки дизайну, 1 блок коду
      </p>
    </section>
  );
}
