import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, CheckSquare, Timer, FolderKanban, BarChart3 } from 'lucide-react';

export const BottomNavigation: React.FC = () => {
  const navItems = [
    { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/tasks', icon: CheckSquare, label: 'Tasks' },
    { to: '/timer', icon: Timer, label: 'Focus' },
    { to: '/projects', icon: FolderKanban, label: 'Projects' },
    { to: '/stats', icon: BarChart3, label: 'Stats' },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-background/80 backdrop-blur-lg border-t border-border px-xs pb-6 pt-2 z-50">
      <div className="max-w-md mx-auto flex justify-between items-center">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) => `flex flex-col items-center gap-1 px-3 py-1 transition-colors ${
              isActive ? 'text-primary-start' : 'text-text-secondary hover:text-text-primary'
            }`}
          >
            <Icon size={24} />
            <span className="text-[10px] font-medium uppercase tracking-wider">{label}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  );
};
