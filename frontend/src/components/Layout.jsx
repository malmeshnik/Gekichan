import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Timer, CheckSquare, BarChart2 } from 'lucide-react';

const Layout = ({ children }) => {
  return (
    <div className="flex flex-col h-screen bg-gray-50 text-gray-900 max-w-md mx-auto relative overflow-hidden">
      <main className="flex-1 overflow-y-auto pb-20">
        {children}
      </main>

      <nav className="fixed bottom-0 left-0 right-0 max-w-md mx-auto bg-white border-t border-gray-200 flex justify-around p-3 z-50">
        <NavLink to="/" className={({ isActive }) => `flex flex-col items-center gap-1 ${isActive ? 'text-blue-600' : 'text-gray-400'}`}>
          <Home size={20} />
          <span className="text-[10px]">Home</span>
        </NavLink>
        <NavLink to="/timer" className={({ isActive }) => `flex flex-col items-center gap-1 ${isActive ? 'text-blue-600' : 'text-gray-400'}`}>
          <Timer size={20} />
          <span className="text-[10px]">Timer</span>
        </NavLink>
        <NavLink to="/tasks" className={({ isActive }) => `flex flex-col items-center gap-1 ${isActive ? 'text-blue-600' : 'text-gray-400'}`}>
          <CheckSquare size={20} />
          <span className="text-[10px]">Tasks</span>
        </NavLink>
        <NavLink to="/stats" className={({ isActive }) => `flex flex-col items-center gap-1 ${isActive ? 'text-blue-600' : 'text-gray-400'}`}>
          <BarChart2 size={20} />
          <span className="text-[10px]">Stats</span>
        </NavLink>
      </nav>
    </div>
  );
};

export default Layout;
