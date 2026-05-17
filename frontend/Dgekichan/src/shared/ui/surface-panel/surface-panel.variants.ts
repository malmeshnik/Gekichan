import { cva } from "class-variance-authority";

export const surfacePanelVariants = cva(
  [
    "transition-standard",
    "radius-card",
  ],
  {
    variants: {
      variant: {
        base: "surface-base",
        default: "surface-card",
        elevated: "surface-card-hover",
        active: "surface-card-active",
        glass: "glass-medium",
        "glass-heavy": "glass-heavy",
      },

      glow: {
        none: "",
        primary: "glow-primary",
        secondary: "glow-secondary",
      },

      interactive: {
        true: "interactive",
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
