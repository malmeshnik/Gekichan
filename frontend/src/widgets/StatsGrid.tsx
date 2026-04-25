import React from 'react';
import { StatCard } from '../shared/ui/StatCard';
import { Flame, Target, Trophy } from 'lucide-react';
import { useStatsStore } from '../entities/statsStore';

export const StatsGrid: React.FC = () => {
  const { today, isLoading } = useStatsStore();

  if (isLoading && !today) {
    return (
      <div className="grid grid-cols-2 gap-md">
        <div className="h-24 bg-card animate-pulse rounded-2xl" />
        <div className="h-24 bg-card animate-pulse rounded-2xl" />
        <div className="h-24 bg-card animate-pulse rounded-2xl col-span-2" />
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 gap-md">
      <StatCard
        label="Tasks Done"
        value={`${today?.completed_tasks_count || 0}`}
        icon={<Target size={16} />}
        className="col-span-1"
      />
      <StatCard
        label="Interruptions"
        value={`${today?.interruptions_count || 0}`}
        subValue="Keep it low!"
        icon={<Flame size={16} className="text-orange-500" />}
        className="col-span-1"
      />
      <StatCard
        label="Focus Time"
        value={`${Math.floor((today?.total_focus_time || 0) / 60)}m`}
        subValue="Today's total"
        icon={<Trophy size={16} className="text-yellow-500" />}
        className="col-span-2"
      />
    </div>
  );
};
