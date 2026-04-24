import React from 'react';
import { Settings, Grid } from 'lucide-react';

interface HeaderProps {
  title: string;
  showMenu?: boolean;
  showSettings?: boolean;
}

export const Header: React.FC<HeaderProps> = ({ title, showMenu = true, showSettings = true }) => {
  return (
    <header className="flex items-center justify-between px-md py-lg sticky top-0 bg-background/80 backdrop-blur-md z-40">
      {showMenu ? (
        <button aria-label="Open menu" className="p-2 text-text-secondary hover:text-text-primary transition-colors">
          <Grid size={24} />
        </button>
      ) : <div className="w-10" />}

      <h1 className="text-lg font-bold tracking-tight">{title}</h1>

      {showSettings ? (
        <button aria-label="Open settings" className="p-2 text-text-secondary hover:text-text-primary transition-colors">
          <Settings size={24} />
        </button>
      ) : <div className="w-10" />}
    </header>
  );
};
