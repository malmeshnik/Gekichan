import React from 'react';
import { Play, Pause, Square } from 'lucide-react';

interface TimerControlsProps {
  isActive: boolean;
  onStart: () => void;
  onPause: () => void;
  onStop: () => void;
  onAdjust: (minutes: number) => void;
}

export const TimerControls: React.FC<TimerControlsProps> = ({
  isActive,
  onStart,
  onPause,
  onStop,
}) => {
  return (
    <div className="flex flex-col items-center gap-lg">
      <div className="flex items-center gap-xl">
        <button
          aria-label="Stop timer"
          onClick={onStop}
          className="p-4 bg-card border border-border rounded-full text-text-secondary hover:text-text-primary transition-colors disabled:opacity-50"
          disabled={!isActive}
        >
          <Square size={24} fill="currentColor" />
        </button>

        <button
          aria-label={isActive ? "Add Interruption" : "Start timer"}
          onClick={isActive ? onPause : onStart}
          className="w-20 h-20 flex items-center justify-center bg-white text-background rounded-full shadow-xl shadow-white/10 active:scale-95 transition-transform"
        >
          {isActive ? <Pause size={32} fill="currentColor" /> : <Play size={32} className="ml-1" fill="currentColor" />}
        </button>

        <button
          aria-label="Placeholder"
          className="p-4 bg-card border border-border rounded-full text-text-secondary hover:text-text-primary transition-colors opacity-20"
          disabled
        >
          <div className="flex items-center">
            <Play size={20} fill="currentColor" />
            <div className="w-[2px] h-4 bg-current ml-[2px]" />
          </div>
        </button>
      </div>

      <div className="text-center">
        {isActive && (
          <p className="text-[10px] font-bold text-text-secondary uppercase tracking-[0.2em]">
            Tap the center button to log an interruption
          </p>
        )}
      </div>
    </div>
  );
};
