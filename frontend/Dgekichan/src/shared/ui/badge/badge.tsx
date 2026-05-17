import { type HTMLAttributes } from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/shared/lib/cn";

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 px-gutter py-1.5 radius-full typography-label border transition-standard",
  {
    variants: {
      variant: {
        default: "bg-surface-container-high text-text-main border-white/10",
        primary: "bg-primary/10 text-primary border-primary/30",
        secondary: "bg-secondary/10 text-secondary border-secondary/30",
        tertiary: "bg-surface-container-high text-accent-secondary border-accent-secondary/30",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}
