import { cva } from "class-variance-authority";

export const buttonVariants = cva(
  [
    "inline-flex",
    "items-center",
    "justify-center",

    "transition-standard",
    "interactive",

    "radius-card",

    "typography-body",

    "border",

    "select-none",
  ],

  {
    variants: {
      variant: {
        primary: [
          "bg-primary",
          "text-background",

          "border-transparent",
        ],

        secondary: [
          "bg-card",
          "text-text-main",

          "border-white/10",
        ],

        ghost: [
          "bg-transparent",
          "text-text-main",

          "border-transparent",
        ],

        danger: [
          "bg-danger",
          "text-white",

          "border-transparent",
        ],
      },

      size: {
        sm: "h-9 px-3",

        md: "h-11 px-4",

        lg: "h-14 px-6",
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