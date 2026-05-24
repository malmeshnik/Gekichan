import { cva } from "class-variance-authority";

export const surfacePanelVariants = cva(
  [
    /*
     * Base
     */
    "relative",

    "overflow-hidden",

    "rounded-card",

    "border",

    "transition-colors",
    "duration-200",

    "will-change-transform",
  ].join(" "),
  {
    variants: {
      variant: {
        /*
         * Minimal surface
         */
        base: [
          "bg-surface",

          "border-outline/30",
        ].join(" "),

        /*
         * Standard card
         */
        default: [
          "bg-surface-container",

          "border-outline/50",
        ].join(" "),

        /*
         * Elevated surface
         */
        elevated: [
          "bg-surface-container-high",

          "border-outline/60",
        ].join(" "),

        /*
         * Active state
         */
        active: [
          "bg-surface-container-highest",

          "border-primary/20",
        ].join(" "),

        /*
         * Main glass card
         * Based on original design
         */
        glass: [
        /*
        * Original glass card from design
        */
        "bg-[rgba(30,41,59,0.6)]",

        /*
        * Blur
        */
        "backdrop-blur-[12px]",

        "supports-[backdrop-filter]:backdrop-blur-[12px]",

        /*
        * Top highlight border
        */
        "border-t",

        "border-white/10",
        ].join(" "),
      },

      glow: {
        none: "",

        primary: [
          "shadow-[0_0_20px_rgba(76,214,255,0.2)]",
        ].join(" "),

        secondary: [
          "shadow-[0_0_20px_rgba(221,183,255,0.2)]",
        ].join(" "),

        ambient: [
          "shadow-[0_0_40px_rgba(76,214,255,0.08)]",
        ].join(" "),
      },

      interactive: {
        true: [
          "cursor-pointer",

          "active:scale-[0.98]",
        ].join(" "),

        false: "",
      },
    },

    compoundVariants: [
      {
        variant: "active",
        interactive: true,

        className:
          "hover:border-primary/30",
      },

      {
        variant: "glass",
        glow: "primary",

        className:
          "border-primary/10",
      },

      {
        variant: "glass",
        glow: "secondary",

        className:
          "border-secondary/10",
      },
    ],

    defaultVariants: {
      variant: "default",

      glow: "none",

      interactive: false,
    },
  }
);