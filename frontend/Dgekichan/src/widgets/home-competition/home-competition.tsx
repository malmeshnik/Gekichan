import { Swords } from "lucide-react";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { StatBar } from "@/shared/ui/stat-bar";

export function HomeCompetition() {
  return (
    <SurfacePanel variant="default" className="section-padding stack-md">
      <h3 className="typography-headline-sm flex items-center gap-[8px]">
        <Swords size={20} className="text-secondary" />
        Мікро-Змагання
      </h3>

      <div className="flex items-end gap-stack-lg mt-stack-sm">
        <StatBar
          label="Ти"
          value="450 XP"
          progress={75}
          className="flex-1"
        />

        <span className="typography-label text-text-muted pb-1 mb-1">VS</span>

        <StatBar
          label="@User99"
          value="320 XP"
          progress={45}
          variant="danger"
          className="flex-1"
        />
      </div>
    </SurfacePanel>
  );
}
