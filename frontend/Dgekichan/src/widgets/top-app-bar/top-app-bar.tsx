import { Flame } from "lucide-react";

import { Badge } from "@/shared/ui/badge";

export function TopAppBar() {
  return (
    <header
      className="
        fixed
        inset-x-0
        top-0
        z-50

        h-16

        border-b
        border-outline/40

        bg-background/60
        backdrop-blur-2xl

        shadow-[var(--shadow-topbar)]
      "
    >
      <div
        className="
          mx-auto
          flex
          h-full
          w-full
          max-w-md
          items-center
          justify-between

          px-container-padding
        "
      >
        {/* Left */}
        <div
          className="
            flex
            items-center
            gap-stack-sm
          "
        >
          {/* Avatar */}
          <div
            className="
              relative

              h-9
              w-9

              overflow-hidden

              rounded-full

              border
              border-outline/50

              bg-surface-container-high

              shadow-[var(--shadow-neon)]
            "
          >
            <img
              alt="User Avatar"
              className="
                h-full
                w-full
                object-cover
              "
              src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
            />

            {/* Neon ring */}
            <div
              className="
                absolute
                inset-0

                rounded-full

                ring-1
                ring-primary/20
              "
            />
          </div>

          {/* Logo */}
          <div className="flex flex-col leading-none">
            <span
              className="
                typography-headline-sm

                text-primary

                tracking-tight
              "
            >
              TaskCommand
            </span>
          </div>
        </div>

        {/* Right */}
        <Badge
          variant="tertiary"
          className="
            h-9

            gap-1.5

            rounded-full

            border
            border-outline/50

            bg-surface-container-high/90

            px-3

            backdrop-blur-xl

            transition-all
            duration-300

            hover:border-secondary/30
            hover:bg-surface-container-highest
          "
        >
          <Flame
            size={14}
            fill="currentColor"
            className="
              text-secondary

              drop-shadow-[0_0_8px_rgba(221,183,255,0.45)]
            "
          />

          <span
            className="
              typography-label

              text-text-main
            "
          >
            12 streak
          </span>
        </Badge>
      </div>
    </header>
  );
}