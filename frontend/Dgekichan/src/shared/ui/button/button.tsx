import type {
  ButtonHTMLAttributes,
} from "react";

import { cn } from "@/shared/lib/cn";

import { buttonVariants } from "./button.variants";

type ButtonProps =
  ButtonHTMLAttributes<HTMLButtonElement> & {
    variant?:
      | "primary"
      | "secondary"
      | "ghost"
      | "danger";

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
    <button
      className={cn(
        buttonVariants({
          variant,
          size,
          fullWidth,
        }),

        className
      )}
      {...props}
    />
  );
}