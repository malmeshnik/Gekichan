import { cva } from "class-variance-authority";

export const buttonVariants = cva(
  [
    /*
     * Layout
     */
    "inline-flex",

    "items-center",
    "justify-center",

    "shrink-0",

    /*
     * Typography
     */
    "typography-body",

    /*
     * Shape
     */
    "rounded-control",

    /*
     * Effects
     */
    "border",

    "transition-colors",
    "duration-200",

    /*
     * UX
     */
    "select-none",
  ].join(" "),

  {
    variants: {
      variant: {
        primary: [
          "bg-primary",

          "text-background",

          "border-transparent",
        ].join(" "),

        secondary: [
          "bg-surface-container-high",

          "text-text-main",

          "border-outline/60",
        ].join(" "),

        ghost: [
          "bg-transparent",

          "text-text-main",

          "border-transparent",

          "hover:bg-surface-container-highest",
        ].join(" "),

        danger: [
          "bg-danger",

          "text-white",

          "border-transparent",
        ].join(" "),

        active: [
          "bg-primary/10",

          "text-primary",

          "border-primary/20",
        ].join(" "),
      },

      size: {
        sm: [
          "h-9",

          "px-3",
        ].join(" "),

        md: [
          "h-11",

          "px-4",
        ].join(" "),

        lg: [
          "h-14",

          "px-6",
        ].join(" "),
      },

      fullWidth: {
        true: "w-full",

        false: "",
      },
    },

    defaultVariants: {
      variant: "primary",

      size: "md",

      fullWidth: false,
    },
  }
);