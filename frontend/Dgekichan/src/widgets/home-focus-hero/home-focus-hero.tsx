import { useState } from "react";
import { Pause, Play } from "lucide-react";
import { motion } from "framer-motion";
import { ProgressRing } from "@/shared/ui/progress-ring";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { Button } from "@/shared/ui/button";

export function HomeFocusHero() {
  const [isActive, setIsActive] = useState(true);

  return (
    <section className="flex flex-col items-center justify-center stack-lg">
      <div className="relative group cursor-pointer" onClick={() => setIsActive(!isActive)}>
        <ProgressRing
          progress={75}
          size={240}
          strokeWidth={8}
          glow={isActive}
          className="transition-all duration-700"
        />
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            animate={{ scale: isActive ? 1.05 : 1 }}
            className="typography-display text-primary drop-shadow-[0_0_16px_var(--primary)]"
          >
            24:15
          </motion.span>
          <span className="typography-label text-text-muted">В процесі</span>
        </div>
      </div>

      <SurfacePanel
        variant="glass"
        glow={isActive ? "primary" : "none"}
        className="w-full section-padding flex justify-between items-center border-l-4 border-l-primary"
      >
        <div className="flex flex-col stack-sm">
          <span className="typography-label text-primary">Дизайн</span>
          <span className="typography-body-lg font-bold">Оновлення UI компонентів</span>
        </div>

        <Button
          variant="secondary"
          className="w-12 h-12 radius-full !p-0"
          onClick={(e) => {
            e.stopPropagation();
            setIsActive(!isActive);
          }}
        >
          {isActive ? <Pause size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" />}
        </Button>
      </SurfacePanel>
    </section>
  );
}
