import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, CheckSquare, Timer, FolderKanban, BarChart3, Settings } from 'lucide-react';
import { useI18n } from '../lib/i18n';

export const BottomNavigation: React.FC = () => {
  const { t } = useI18n();
  const navItems = [
    { to: '/', icon: LayoutDashboard, label: t('dashboard') },
    { to: '/tasks', icon: CheckSquare, label: t('tasks') },
    { to: '/timer', icon: Timer, label: t('timer') },
    { to: '/projects', icon: FolderKanban, label: t('projects') },
    { to: '/stats', icon: BarChart3, label: t('stats') },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-background/80 backdrop-blur-lg border-t border-border px-xs pb-safe-area-inset-bottom pt-2 z-50">
      <div className="max-w-md mx-auto flex justify-around items-center">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) => `flex flex-col items-center gap-1 px-1 py-1 transition-colors ${
              isActive ? 'text-primary-start' : 'text-text-secondary hover:text-text-primary'
            }`}
          >
            <Icon size={20} />
            <span className="text-[8px] font-medium uppercase tracking-tight">{label}</span>
          </NavLink>
        ))}
      </div>
    </nav>
  );
};
