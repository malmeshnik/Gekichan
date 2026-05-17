import { Shield, ChevronRight } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";

export function HomeStyleCard() {
  return (
    <SurfacePanel
      variant="default"
      className="section-padding flex items-center justify-between border-l-4 border-l-accent-secondary interactive"
      interactive
    >
      <div className="flex items-center gap-stack-md">
        <div className="w-12 h-12 radius-full bg-accent-secondary/10 flex items-center justify-center text-accent-secondary">
          <Shield size={24} />
        </div>
        <div className="flex flex-col stack-sm">
          <span className="typography-label text-text-muted">Твій Стиль</span>
          <span className="typography-body-lg font-bold">Стабільний Виконавець</span>
        </div>
      </div>

      <ChevronRight size={20} className="text-text-muted" />
    </SurfacePanel>
  );
}
