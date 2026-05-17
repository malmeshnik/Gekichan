import { Flame } from "lucide-react";
import { Badge } from "@/shared/ui/badge";

export function TopAppBar() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-16 px-container-padding glass-heavy flex justify-between items-center border-b border-white/5">
      <div className="flex items-center gap-gutter">
        <div className="w-10 h-10 rounded-full bg-surface-container-high overflow-hidden border border-outline/30 shadow-inner">
           <img
            alt="User Avatar"
            className="w-full h-full object-cover"
            src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
          />
        </div>
        <h1 className="typography-headline text-primary">TaskCommand</h1>
      </div>

      <Badge variant="tertiary" className="h-9 px-container-padding">
        <Flame size={16} fill="var(--accent-secondary)" className="text-accent-secondary" />
        <span className="font-bold">12 streak</span>
      </Badge>
    </header>
  );
}
