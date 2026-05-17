import { Rocket } from "lucide-react";
import { StatBar } from "@/shared/ui/stat-bar";
import { SurfacePanel } from "@/shared/ui/surface-panel";

export function HomeSmartStart() {
  return (
    <SurfacePanel variant="default" className="p-6 flex flex-col gap-6 relative overflow-hidden group">
      {/* Background bloom */}
      <div className="absolute -right-8 -top-8 w-24 h-24 bg-primary/5 blur-3xl pointer-events-none group-hover:bg-primary/10 transition-all duration-700" />

      <div className="flex justify-between items-start relative z-10">
        <div className="flex flex-col gap-1">
          <h2 className="typography-headline-sm text-text-main/90">Розумний Старт</h2>
          <p className="text-xs text-text-muted/80">Вчора 2.8г, Ціль 3г</p>
        </div>
        <div className="bg-white/5 text-primary/80 p-2.5 radius-2xl border border-white/5">
          <Rocket size={18} />
        </div>
      </div>

      <StatBar
        progress={85}
        value="Залишилося 15 хв"
        className="relative z-10"
      />
    </SurfacePanel>
  );
}
