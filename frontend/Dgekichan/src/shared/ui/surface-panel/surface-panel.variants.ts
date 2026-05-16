import { cva } from "class-variance-authority";

export const surfacePanelVariants = cva(
  [
    "transition-standard",
    "radius-card",
  ],
  {
    variants: {
      variant: {
        default: "surface-card",

        hover: "surface-card-hover",

        active: "surface-card-active",

        glass: "glass-medium",
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