import type { HTMLAttributes } from "react";
import { motion } from "framer-motion";
import { cn } from "@/shared/lib/cn";

import { surfacePanelVariants } from "./surface-panel.variants";

type SurfacePanelProps =
  HTMLAttributes<HTMLDivElement> & {
    variant?:
      | "base"
      | "default"
      | "elevated"
      | "active"
      | "glass"
      | "glass-heavy";

    glow?:
      | "none"
      | "primary"
      | "secondary";

    interactive?: boolean;
  };

export function SurfacePanel({
  className,
  variant,
  glow,
  interactive,
  ...props
}: SurfacePanelProps) {
  const Component = interactive ? motion.div : "div";

  const interactionProps = interactive ? {
    whileHover: { y: -2, transition: { duration: 0.2 } },
    whileTap: { scale: 0.98 },
  } : {};

  return (
    <Component
      className={cn(
        surfacePanelVariants({
          variant,
          glow,
          interactive,
        }),
        className
      )}
      {...interactionProps as any}
      {...props as any}
    />
  );
}
