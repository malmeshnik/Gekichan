import type {
  ButtonHTMLAttributes,
} from "react";
import { motion, type HTMLMotionProps } from "framer-motion";
import { cn } from "@/shared/lib/cn";

import { buttonVariants } from "./button.variants";

type ButtonProps =
  Omit<HTMLMotionProps<"button">, keyof ButtonHTMLAttributes<HTMLButtonElement>> &
  ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?:
      | "primary"
      | "secondary"
      | "ghost"
      | "danger"
      | "active";

    size?:
      | "sm"
      | "md"
      | "lg";

    fullWidth?: boolean;
  };

export function Button({
  className,

  variant,
  size,
  fullWidth,

  ...props
}: ButtonProps) {
  return (
    <motion.button
      whileTap={{ scale: 0.96 }}
      whileHover={{ scale: 1.02 }}
      className={cn(
        buttonVariants({
          variant,
          size,
          fullWidth,
        }),

        className
      )}
      {...props as any}
    />
  );
}
