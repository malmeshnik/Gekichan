import { Zap, ListTodo, LayoutGrid, BarChart3 } from "lucide-react";
import { BottomDock, BottomDockItem } from "@/shared/ui/bottom-dock";

export function BottomNavigation() {
  return (
    <BottomDock>
      <BottomDockItem
        icon={<Zap size={24} />}
        label="Focus"
        active
      />
      <BottomDockItem
        icon={<ListTodo size={24} />}
        label="Tasks"
      />
      <BottomDockItem
        icon={<LayoutGrid size={24} />}
        label="Projects"
      />
      <BottomDockItem
        icon={<BarChart3 size={24} />}
        label="Stats"
      />
    </BottomDock>
  );
}
