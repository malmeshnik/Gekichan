import React from 'react';

interface TimerDisplayProps {
  seconds: number;
  label?: string;
}

export const TimerDisplay: React.FC<TimerDisplayProps> = ({ seconds, label = 'REMAINING' }) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;

  const formattedMins = mins.toString().padStart(2, '0');
  const formattedSecs = secs.toString().padStart(2, '0');

  return (
    <div className="flex flex-col items-center">
      <span className="text-6xl font-bold tracking-tighter tabular-nums">
        {formattedMins}:{formattedSecs}
      </span>
      {label && (
        <span className="text-xs font-semibold text-text-secondary tracking-[0.2em] mt-2">
          {label}
        </span>
      )}
    </div>
  );
};
