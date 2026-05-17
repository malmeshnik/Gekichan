import { Rocket } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { StatBar } from "@/shared/ui/stat-bar";

export function HomeSmartStart() {
  return (
    <SurfacePanel variant="default" className="section-padding stack-md">
      <div className="flex justify-between items-start">
        <div className="stack-sm">
          <h2 className="typography-headline-sm text-primary-soft">Розумний Старт</h2>
          <p className="typography-body text-text-muted">Вчора 2.8г, Ціль 3г</p>
        </div>
        <div className="bg-surface-container-highest text-primary p-[8px] radius-card">
          <Rocket size={20} />
        </div>
      </div>

      <StatBar
        progress={85}
        value="Залишилося 15 хв"
      />
    </SurfacePanel>
  );
}
