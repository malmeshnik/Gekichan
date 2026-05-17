import { cva } from "class-variance-authority";

export const surfacePanelVariants = cva(
  [
    "transition-standard",
    "radius-3xl",
  ],
  {
    variants: {
      variant: {
        base: "surface-base",
        default: "surface-card bg-surface-base/30",
        elevated: "surface-card-hover bg-surface-elevated/40",
        active: "surface-card-active bg-surface-floating/50",
        glass: "surface-matte-glass",
        "glass-heavy": "surface-matte-glass shadow-[0_8px_32px_rgba(0,0,0,0.6)]",
      },

      glow: {
        none: "",
        primary: "glow-primary",
        secondary: "glow-secondary",
        ambient: "glow-ambient",
      },

      interactive: {
        true: "interactive cursor-pointer",
        false: "",
      },
    },

    defaultVariants: {
      variant: "default",
      glow: "none",
      interactive: false,
    },
  }
);
