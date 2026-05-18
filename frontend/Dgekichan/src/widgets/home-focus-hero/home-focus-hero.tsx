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
    <section className="flex flex-col items-center justify-center">
      {/* Timer Container */}
      <div
        className="relative group cursor-pointer flex items-center justify-center"
        onClick={() => setIsActive(!isActive)}
      >
        <ProgressRing
          progress={75}
          size={200}
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
      <div className="w-full mt-stack-md">
        <SurfacePanel
          variant="glass"
          className="
            flex
            w-full
            items-center
            justify-between

            border-l-4
            border-l-primary

            p-4
          "
        >
          {/* Left */}
          <div
            className="
              flex
              flex-col
            "
          >
            <span
              className="
                typography-label

                uppercase

                text-primary-soft
              "
            >
              Дизайн
            </span>

            <span
              className="
                typography-body-lg

                font-semibold

                text-text-main
              "
            >
              Оновлення UI компонентів
            </span>
          </div>

          {/* Action */}
          <Button
            variant="ghost"
            className={cn(
              `
                flex
                h-10
                w-10
                items-center
                justify-center

                rounded-full

                border
                border-outline/60

                bg-surface-container-highest

                text-primary

                transition-colors

                hover:bg-surface-container-high
              `,

              !isActive && "text-primary-soft"
            )}
            onClick={(e) => {
              e.stopPropagation();

              setIsActive(!isActive);
            }}
          >
            <AnimatePresence mode="wait">
              <motion.div
                key={isActive ? "pause" : "play"}
                initial={{
                  opacity: 0,
                  scale: 0.8,
                }}
                animate={{
                  opacity: 1,
                  scale: 1,
                }}
                exit={{
                  opacity: 0,
                  scale: 0.8,
                }}
                transition={{
                  duration: 0.2,
                }}
              >
                {isActive ? (
                  <Pause
                    size={18}
                    className="fill-current"
                  />
                ) : (
                  <Play
                    size={18}
                    className="ml-0.5 fill-current"
                  />
                )}
              </motion.div>
            </AnimatePresence>
          </Button>
        </SurfacePanel>
      </div>
    </section>
  );
}
