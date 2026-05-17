import { useState } from "react";
import { Pause, Play } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { ProgressRing } from "@/shared/ui/progress-ring";
import { Button } from "@/shared/ui/button";
import { SurfacePanel } from "@/shared/ui/surface-panel";
import { cn } from "@/shared/lib/cn";

export function HomeFocusHero() {
  const [isActive, setIsActive] = useState(true);

  return (
    <section className="flex flex-col items-center justify-center pt-20 pb-16">
      {/* Timer Container */}
      <div
        className="relative group cursor-pointer flex items-center justify-center"
        onClick={() => setIsActive(!isActive)}
      >
        <ProgressRing
          progress={75}
          size={300}
          strokeWidth={6}
          glow={isActive}
          className="transition-all duration-1000"
        />

        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            animate={{
              scale: isActive ? 1.02 : 1,
              opacity: isActive ? 1 : 0.8
            }}
            className="typography-display text-text-main"
          >
            24:15
          </motion.span>
          <span className="typography-label text-text-muted mt-2 opacity-60">
            {isActive ? "в процесі" : "пауза"}
          </span>
        </div>
      </div>

      {/* Active Task Card */}
      <div className="w-full mt-16 px-4">
        <SurfacePanel variant="glass" className="p-5 flex justify-between items-center relative overflow-hidden">
          {/* Subtle Ambient Light behind task */}
          <div className="absolute -left-12 top-0 bottom-0 w-24 bg-primary/5 blur-2xl pointer-events-none" />

          <div className="flex flex-col gap-1 relative z-10">
            <div className="flex items-center gap-2">
               <div className="w-1 h-1 rounded-full bg-primary" />
               <span className="typography-label text-primary opacity-60">Дизайн</span>
            </div>
            <span className="text-base font-medium text-text-main tracking-tight">Оновлення UI компонентів</span>
          </div>

          <Button
            variant="ghost"
            className={cn(
              "w-12 h-12 radius-full bg-white/5 border border-white/5 hover:bg-white/10 transition-all duration-500",
              !isActive && "text-primary"
            )}
            onClick={(e) => {
              e.stopPropagation();
              setIsActive(!isActive);
            }}
          >
            <AnimatePresence mode="wait">
              <motion.div
                key={isActive ? "pause" : "play"}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.2 }}
              >
                {isActive ? <Pause size={20} className="fill-current" /> : <Play size={20} className="ml-1 fill-current" />}
              </motion.div>
            </AnimatePresence>
          </Button>
        </SurfacePanel>
      </div>
    </section>
  );
}
