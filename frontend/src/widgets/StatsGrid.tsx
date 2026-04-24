import React from 'react';
import { StatCard } from '../shared/ui/StatCard';
import { Flame, Target, Trophy } from 'lucide-react';

export const StatsGrid: React.FC = () => {
  return (
    <div className="grid grid-cols-2 gap-md">
      <StatCard
        label="Tasks"
        value="8/12"
        icon={<Target size={16} />}
        className="col-span-1"
      />
      <StatCard
        label="Streak"
        value="5 Days"
        subValue="Keep it up!"
        icon={<Flame size={16} className="text-orange-500" />}
        className="col-span-1"
      />
      <StatCard
        label="Best Focus Session"
        value="90m"
        subValue="Deep Work Block"
        icon={<Trophy size={16} className="text-yellow-500" />}
        className="col-span-2"
      />
    </div>
  );
};
