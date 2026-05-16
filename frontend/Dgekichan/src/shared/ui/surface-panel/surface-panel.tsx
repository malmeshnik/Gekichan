import type { HTMLAttributes } from "react";

import { cn } from "@/shared/lib/cn";

import { surfacePanelVariants } from "./surface-panel.variants";

type SurfacePanelProps =
  HTMLAttributes<HTMLDivElement> & {
    variant?:
      | "default"
      | "hover"
      | "active"
      | "glass";

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
  return (
    <div
      className={cn(
        surfacePanelVariants({
          variant,
          glow,
          interactive,
        }),
        className
      )}
      {...props}
    />
  );
}