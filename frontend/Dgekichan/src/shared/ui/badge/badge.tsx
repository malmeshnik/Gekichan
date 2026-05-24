import { type HTMLAttributes } from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/shared/lib/cn";

const badgeVariants = cva(
  [
    "inline-flex",
    "items-center",
    "justify-center",

    "gap-1.5",

    "px-3",
    "py-1.5",

    "rounded-full",

    "border",

    "typography-label",

    "transition-all",
    "duration-300",

    "backdrop-blur-xl",

    "select-none",
    "whitespace-nowrap",
  ].join(" "),
  {
    variants: {
      variant: {
        default: [
          "bg-surface-container-high/80",

          "text-text-main",

          "border-outline/50",

          "hover:bg-surface-container-highest",
        ].join(" "),

        primary: [
          "bg-primary/10",

          "text-primary",

          "border-primary/20",

          "shadow-[0_0_12px_rgba(76,214,255,0.12)]",

          "hover:bg-primary/15",
          "hover:border-primary/30",
        ].join(" "),

        secondary: [
          "bg-secondary/10",

          "text-secondary",

          "border-secondary/20",

          "shadow-[0_0_12px_rgba(221,183,255,0.12)]",

          "hover:bg-secondary/15",
          "hover:border-secondary/30",
        ].join(" "),

        tertiary: [
          "bg-surface-container-high/90",

          "text-accent-secondary",

          "border-accent-secondary/20",

          "shadow-[0_0_12px_rgba(203,162,255,0.12)]",

          "hover:bg-surface-container-highest",
          "hover:border-accent-secondary/30",
        ].join(" "),

        success: [
          "bg-emerald-500/10",

          "text-emerald-300",

          "border-emerald-400/20",

          "shadow-[0_0_12px_rgba(52,211,153,0.12)]",
        ].join(" "),

        danger: [
          "bg-danger/10",

          "text-danger",

          "border-danger/20",

          "shadow-[0_0_12px_rgba(255,123,114,0.12)]",
        ].join(" "),
      },

      size: {
        sm: [
          "h-7",

          "px-2.5",

          "text-[11px]",
        ].join(" "),

        md: [
          "h-8",

          "px-3",
        ].join(" "),

        lg: [
          "h-10",

          "px-4",

          "text-sm",
        ].join(" "),
      },
    },

    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
);

export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({
  className,
  variant,
  size,
  ...props
}: BadgeProps) {
  return (
    <span
      className={cn(
        badgeVariants({
          variant,
          size,
        }),
        className
      )}
      {...props}
    />
  );
}