import { motion, AnimatePresence } from "framer-motion";
import { useState, useMemo } from "react";
import { SurfacePanel } from "@/shared/ui/surface-panel/surface-panel";
import type { ChartDataItem } from "@/entities/stats/statsStore";
import { formatFocusTime } from "@/shared/lib/format/time";
import { cn } from "@/shared/lib/cn";

interface ProductivityChartProps {
  data: ChartDataItem[];
  period: string;
}

export function ProductivityChart({ data, period }: ProductivityChartProps) {
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);

  const maxFocus = useMemo(() => {
    const m = Math.max(...data.map((d) => d.focus_time), 0);
    return m > 0 ? m : 3600;
  }, [data]);

  // Simplify labels for better fit
  const displayData = useMemo(() => {
    if (period === "month") {
      // For month, show only every 5th label or start/end
      return data.map((d, i) => ({
        ...d,
        showLabel: i % 5 === 0 || i === data.length - 1
      }));
    }
    if (period === "day") {
        // For day, show every 4th hour
        return data.map((d, i) => ({
            ...d,
            showLabel: i % 4 === 0 || i === 23
        }));
    }
    return data.map(d => ({ ...d, showLabel: true }));
  }, [data, period]);

  return (
    <SurfacePanel className="p-4 flex flex-col gap-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-white">Продуктивність</h3>
        <div className="flex flex-col items-end">
            <span className="text-[10px] text-white/20 uppercase font-bold">Макс. фокус</span>
            <span className="text-xs text-white/60">{formatFocusTime(maxFocus)}</span>
        </div>
      </div>

      <div className="relative flex items-end justify-between h-48 gap-1 px-1">
        {/* Y-Axis lines (optional for depth) */}
        <div className="absolute inset-x-0 top-0 bottom-8 flex flex-col justify-between pointer-events-none opacity-5">
            <div className="w-full h-px bg-white" />
            <div className="w-full h-px bg-white" />
            <div className="w-full h-px bg-white" />
        </div>

        {displayData.map((item, idx) => {
          const height = (item.focus_time / maxFocus) * 100;
          const isSelected = selectedIdx === idx;

          return (
            <div
                key={idx}
                className="flex flex-col items-center flex-1 gap-2 h-full justify-end group cursor-pointer"
                onClick={() => setSelectedIdx(isSelected ? null : idx)}
            >
              <div className="relative w-full flex flex-col items-center flex-1 justify-end">
                <AnimatePresence>
                    {isSelected && (
                        <motion.div
                            initial={{ opacity: 0, y: 10, scale: 0.9 }}
                            animate={{ opacity: 1, y: -4, scale: 1 }}
                            exit={{ opacity: 0, y: 10, scale: 0.9 }}
                            className="absolute bottom-full mb-2 z-20 whitespace-nowrap bg-surface-floating border border-white/10 px-2 py-1 rounded shadow-xl"
                        >
                            <span className="text-[10px] font-bold text-primary">{formatFocusTime(item.focus_time)}</span>
                        </motion.div>
                    )}
                </AnimatePresence>

                <motion.div
                  initial={{ height: 0 }}
                  animate={{ height: `${Math.max(height, 2)}%` }}
                  className={cn(
                    "w-full max-w-[12px] rounded-t-sm relative transition-colors",
                    isSelected ? "bg-primary" : "bg-primary/40 group-hover:bg-primary/60"
                  )}
                >
                </motion.div>

                <div className="w-full h-[2px] bg-white/5 rounded-full mt-1 overflow-hidden">
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.min(height, 100)}%` }}
                        className={cn(
                            "h-full rounded-full transition-colors",
                            isSelected ? "bg-primary shadow-[0_0_8px_rgba(var(--primary-rgb),0.5)]" : "bg-primary/20"
                        )}
                    />
                </div>
              </div>
              <span className={cn(
                "text-[8px] uppercase transition-colors",
                item.showLabel ? "text-white/40" : "text-transparent",
                isSelected && "text-primary font-bold"
              )}>
                {item.label}
              </span>
            </div>
          );
        })}
      </div>

      {selectedIdx !== null && (
          <div className="flex justify-between items-center px-2 py-2 bg-white/5 rounded-lg border border-white/5">
              <div className="flex flex-col">
                  <span className="text-[10px] text-white/40 uppercase font-bold">Дата/Період</span>
                  <span className="text-xs text-white">{displayData[selectedIdx].label}</span>
              </div>
              <div className="flex flex-col items-end">
                  <span className="text-[10px] text-white/40 uppercase font-bold">Час фокусу</span>
                  <span className="text-xs text-primary font-bold">{formatFocusTime(displayData[selectedIdx].focus_time)}</span>
              </div>
          </div>
      )}
    </SurfacePanel>
  );
}
