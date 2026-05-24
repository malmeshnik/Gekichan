import { motion } from "framer-motion";
import { cn } from "@/shared/lib/cn";

interface ProgressRingProps {
  progress: number; // 0 to 100
  size?: number;
  strokeWidth?: number;
  className?: string;
  glow?: boolean;
}

export function ProgressRing({
  progress,
  size = 192,
  strokeWidth = 6,
  className,
  glow = true,
}: ProgressRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className={cn("relative", className)} style={{ width: size, height: size }}>
      {/* Outer Glow Bloom */}
      {glow && (
        <div
          className="absolute inset-0 rounded-full bg-primary/5 blur-[40px] transition-opacity duration-1000"
          style={{ width: size, height: size }}
        />
      )}

      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${size} ${size}`}
        className="transform -rotate-90 relative z-10"
      >
        {/* Soft Energy Track (Background) */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="transparent"
          stroke="rgba(255, 255, 255, 0.03)"
          strokeWidth={strokeWidth}
          className="shadow-inner"
        />

        {/* Recessed Track Shadow (Inner) */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="transparent"
          stroke="rgba(0, 0, 0, 0.2)"
          strokeWidth={strokeWidth - 2}
        />

        {/* Matte Progress Bar */}
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="transparent"
          stroke="var(--primary)"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1.5, ease: [0.4, 0, 0.2, 1] }}
          strokeLinecap="round"
          className={cn(
            "opacity-80",
            glow && "drop-shadow-[0_0_8px_rgba(76,214,255,0.15)]"
          )}
        />
      </svg>
    </div>
  );
}
