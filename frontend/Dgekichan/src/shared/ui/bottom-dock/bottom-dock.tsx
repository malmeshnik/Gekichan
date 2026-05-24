import { motion } from "framer-motion";

import { type ReactNode } from "react";

import { cn } from "@/shared/lib/cn";

interface BottomDockProps {
  children: ReactNode;

  className?: string;
}

export function BottomDock({
  children,
  className,
}: BottomDockProps) {
  return (
    <div
      className="
        fixed
        inset-x-0
        bottom-0

        z-50
      "
    >
      <nav
        className={cn(
          `
            flex
            h-16
            w-full
            items-center
            justify-around

            border-t
            border-white/5

            bg-surface-container/80

            px-4

            pb-safe

            backdrop-blur-xl

            shadow-[0_-4px_24px_rgba(0,0,0,0.5)]
          `,

          className
        )}
      >
        {children}
      </nav>
    </div>
  );
}

interface BottomDockItemProps {
  icon: ReactNode;

  label: string;

  active?: boolean;

  onClick?: () => void;
}

export function BottomDockItem({
  icon,

  label,

  active,

  onClick,
}: BottomDockItemProps) {
  return (
    <motion.button
      whileTap={{
        scale: 0.9,
      }}
      onClick={onClick}
      className={cn(
        `
          relative

          flex
          flex-col
          items-center
          justify-center

          rounded-xl

          px-3
          py-1

          transition-colors
          duration-200
        `,

        active
          ? `
              bg-primary/15

              text-primary
            `
          : `
              text-text-muted

              hover:text-primary
            `
      )}
    >
      {/* Active Background */}
      {active && (
        <motion.div
          layoutId="bottom-dock-active"
          className="
            absolute
            inset-0

            rounded-xl

            border
            border-primary/10

            bg-primary/10
          "
          transition={{
            type: "spring",
            bounce: 0.15,
            duration: 0.5,
          }}
        />
      )}

      {/* Content */}
      <div
        className="
          relative
          z-10

          flex
          flex-col
          items-center
        "
      >
        <div>{icon}</div>

        <span
          className="
            mt-1

            typography-label
          "
        >
          {label}
        </span>
      </div>
    </motion.button>
  );
}