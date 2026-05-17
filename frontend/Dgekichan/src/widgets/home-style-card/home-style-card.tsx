import { Shield, ChevronRight } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";

export function HomeStyleCard() {
  return (
    <SurfacePanel
      interactive
      variant="default"
      className="p-6 flex items-center justify-between relative overflow-hidden group hover:bg-surface-elevated/40 transition-all duration-500"
    >
      {/* Decorative side accent */}
      <div className="absolute left-0 top-4 bottom-4 w-1 bg-secondary/40 radius-full" />

      <div className="flex items-center gap-4 relative z-10">
        <div className="w-12 h-12 radius-2xl bg-white/5 border border-white/5 flex items-center justify-center text-secondary/80 group-hover:scale-110 transition-transform duration-500">
          <Shield size={22} />
        </div>
        <div className="flex flex-col gap-0.5">
          <span className="typography-label text-text-muted/60">Твій Стиль</span>
          <span className="text-base font-medium text-text-main/90 tracking-tight">Стабільний Виконавець</span>
        </div>
      </div>

      <div className="w-8 h-8 radius-full bg-white/5 flex items-center justify-center text-text-muted/40 group-hover:text-text-main group-hover:bg-white/10 transition-all">
        <ChevronRight size={18} />
      </div>
    </SurfacePanel>
  );
}
