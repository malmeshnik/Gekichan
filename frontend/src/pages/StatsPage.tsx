import React from 'react';
import { Header } from '../shared/ui/Header';
import { Card } from '../shared/ui/Card';
import { StatCard } from '../shared/ui/StatCard';
import { Sun, Star, ArrowUpRight } from 'lucide-react';

export const StatsPage: React.FC = () => {
  return (
    <div className="pb-32 min-h-screen">
      <Header title="Productivity" />

      <main className="px-md flex flex-col gap-lg">
        {/* Main Score */}
        <Card className="flex flex-col items-center py-xl">
           <span className="text-xs font-bold text-text-secondary uppercase tracking-widest mb-4">Productivity Score</span>
           <div className="flex items-baseline">
             <span className="text-6xl font-bold">85</span>
             <span className="text-xl text-text-secondary font-medium ml-1">/100</span>
           </div>
           <div className="flex items-center gap-1 text-green-500 font-medium mt-4">
             <ArrowUpRight size={16} />
             <span>+5% from last week</span>
           </div>
        </Card>

        {/* Secondary Stats */}
        <div className="grid grid-cols-2 gap-md">
          <StatCard
            label="Peak Hour"
            value="10:00 AM"
            subValue="Deep Work"
            icon={<Sun size={20} className="text-orange-400" />}
          />
          <StatCard
            label="Best Day"
            value="Tuesday"
            subValue="Most Productive"
            icon={<Star size={20} className="text-blue-400" />}
          />
        </div>

        {/* Focus Trend */}
        <Card>
          <div className="flex items-center justify-between mb-6">
            <div>
              <h4 className="text-xs font-bold text-text-secondary uppercase tracking-widest">Focus Trend</h4>
              <p className="text-[10px] text-text-secondary mt-1">Steady improvement over the last 7 days.</p>
            </div>
            <div className="flex items-center gap-1 text-orange-500 font-bold text-xs">
              <ArrowUpRight size={14} /> 12%
            </div>
          </div>

          <div className="flex items-end justify-between h-32 px-xs">
            {['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((day, i) => (
              <div key={i} className="flex flex-col items-center gap-2 flex-1">
                <div
                  className={`w-1 rounded-full ${i === 1 ? 'bg-primary-start' : 'bg-border'}`}
                  style={{ height: `${[40, 90, 60, 70, 85, 30, 45][i]}%` }}
                />
                <span className="text-[10px] font-bold text-text-secondary">{day}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Tasks by Project */}
        <Card>
           <h4 className="text-xs font-bold text-text-secondary uppercase tracking-widest mb-6">Tasks by Project</h4>
           <div className="flex flex-col gap-lg">
             {[
               { name: 'Design System', tasks: 12, percentage: 45, color: 'bg-blue-500' },
               { name: 'Q3 Marketing', tasks: 8, percentage: 30, color: 'bg-orange-500' },
               { name: 'Admin & Setup', tasks: 6, percentage: 25, color: 'bg-purple-500' },
             ].map((project, i) => (
               <div key={i} className="flex items-center justify-between">
                 <div className="flex items-center gap-md">
                   <div className={`w-1 h-6 rounded-full ${project.color}`} />
                   <div>
                     <h5 className="text-sm font-bold">{project.name}</h5>
                     <p className="text-[10px] text-text-secondary font-medium">{project.tasks} Tasks</p>
                   </div>
                 </div>
                 <span className="text-lg font-bold">{project.percentage}%</span>
               </div>
             ))}
           </div>
        </Card>
      </main>
    </div>
  );
};
