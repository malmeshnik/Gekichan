import { Swords } from "lucide-react";
import { StatBar } from "@/shared/ui/stat-bar";
import { SurfacePanel } from "@/shared/ui/surface-panel";

export function HomeCompetition() {
  return (
    <SurfacePanel variant="default" className="p-6 flex flex-col gap-8 relative overflow-hidden group">
       {/* Background bloom */}
      <div className="absolute -left-8 -bottom-8 w-24 h-24 bg-secondary/5 blur-3xl pointer-events-none group-hover:bg-secondary/10 transition-all duration-700" />

      <h3 className="typography-headline-sm flex items-center gap-2.5 text-text-main/90 relative z-10">
        <div className="p-2 bg-white/5 radius-xl border border-white/5 text-secondary">
          <Swords size={16} />
        </div>
        Мікро-Змагання
      </h3>

      <div className="flex items-center gap-6 relative z-10">
        <StatBar
          label="Ти"
          value="450 XP"
          progress={75}
          className="flex-1"
        />

        <div className="text-[10px] font-bold text-text-muted/40 uppercase tracking-tighter pt-1.5">VS</div>

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
