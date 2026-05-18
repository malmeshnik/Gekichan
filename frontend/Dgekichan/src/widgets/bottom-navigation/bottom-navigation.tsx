import { Zap, ListTodo, LayoutGrid, BarChart3 } from "lucide-react";
import { BottomDock, BottomDockItem } from "@/shared/ui/bottom-dock";
import { useNavigate, useLocation } from "react-router-dom";

export function BottomNavigation() {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <BottomDock>
      <BottomDockItem
        icon={<Zap size={24} />}
        label="Focus"
        active={location.pathname === "/"}
        onClick={() => navigate("/")}
      />
      <BottomDockItem
        icon={<ListTodo size={24} />}
        label="Tasks"
        active={location.pathname === "/tasks"}
        onClick={() => navigate("/tasks")}
      />
      <BottomDockItem
        icon={<LayoutGrid size={24} />}
        label="Projects"
        active={location.pathname === "/projects"}
        onClick={() => navigate("/projects")}
      />
      <BottomDockItem
        icon={<BarChart3 size={24} />}
        label="Stats"
        active={location.pathname === "/stats"}
        onClick={() => navigate("/stats")}
      />
    </BottomDock>
  );
}
