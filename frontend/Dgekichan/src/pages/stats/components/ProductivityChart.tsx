import { motion } from "framer-motion";
import { SurfacePanel } from "@/shared/ui/surface-panel/surface-panel";
import type { ChartDataItem } from "@/entities/stats/statsStore";

interface ProductivityChartProps {
  data: ChartDataItem[];
  period: string;
}

export function ProductivityChart({ data, period }: ProductivityChartProps) {
  const maxFocus = Math.max(...data.map((d) => d.focus_time), 3600); // at least 1h for scale

  const getDayName = (label: string) => {
    // Basic mapping for days if label is 01.01 etc
    return label;
  };

  return (
    <SurfacePanel className="p-4 flex flex-col gap-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold text-white">Продуктивність</h3>
        <div className="text-xs text-white/40">год</div>
      </div>

      <div className="flex items-end justify-between h-40 gap-2 px-1">
        {data.map((item, idx) => {
          const height = (item.focus_time / maxFocus) * 100;
          return (
            <div key={idx} className="flex flex-col items-center flex-1 gap-2">
              <div className="relative w-full flex flex-col items-center group">
                {/* Focus Time Bar */}
                <motion.div
                  initial={{ height: 0 }}
                  animate={{ height: `${height}%` }}
                  className="w-full max-w-[12px] bg-primary rounded-t-sm relative"
                >
                    {/* Tooltip or indicator could go here */}
                </motion.div>

                {/* Underline for focus time indicator as in screenshot */}
                <div className="w-full h-[2px] bg-white/10 rounded-full mt-1">
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.min(height, 100)}%` }}
                        className="h-full bg-primary rounded-full"
                    />
                </div>
              </div>
              <span className="text-[10px] text-white/40 uppercase">
                {item.label}
              </span>
            </div>
          );
        })}
      </div>
    </SurfacePanel>
  );
}
