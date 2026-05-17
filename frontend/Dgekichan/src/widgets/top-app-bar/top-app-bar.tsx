import { Flame } from "lucide-react";
import { Badge } from "@/shared/ui/badge";

export function TopAppBar() {
  return (
    <header className="fixed top-3 left-4 right-4 z-50 h-14 px-4 glass-light radius-full flex justify-between items-center border border-white/5 shadow-lg">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-surface-elevated overflow-hidden border border-white/5">
           <img
            alt="User Avatar"
            className="w-full h-full object-cover"
            src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
          />
        </div>
        <h1 className="text-sm font-semibold tracking-tight text-text-main">TaskCommand</h1>
      </div>

      <Badge variant="tertiary" className="h-8 px-3 bg-surface-elevated/50 border-white/5">
        <Flame size={14} fill="var(--secondary)" className="text-secondary opacity-80" />
        <span className="text-xs font-medium text-text-main">12 streak</span>
      </Badge>
    </header>
  );
}
