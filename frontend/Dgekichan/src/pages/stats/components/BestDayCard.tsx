import { SurfacePanel } from "@/shared/ui/surface-panel/surface-panel";
import { Trophy, Star } from "lucide-react";

interface BestDayCardProps {
  date: string | null;
  score?: number;
}

export function BestDayCard({ date }: BestDayCardProps) {
  if (!date || typeof date === 'object') return null;

  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) return null;

  const formattedDate = dateObj.toLocaleDateString('uk-UA', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });

  return (
    <SurfacePanel
        variant="glass"
        className="p-4 flex items-center gap-4 relative overflow-hidden"
    >
      <div className="absolute -right-4 -top-4 opacity-10 rotate-12">
        <Trophy size={80} className="text-primary" />
      </div>

      <div className="p-3 rounded-full bg-primary/10 text-primary">
        <Star size={24} fill="currentColor" />
      </div>

      <div className="flex flex-col">
        <span className="text-xs text-white/40 uppercase font-bold tracking-wider">Найбільш продуктивний день</span>
        <span className="text-lg font-semibold text-white">{formattedDate}</span>
      </div>
    </SurfacePanel>
  );
}
