import React from 'react';
import { Play, Pause, Square, Plus, Minus } from 'lucide-react';
import { Button } from '../../shared/ui/Button';

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
  onAdjust,
}) => {
  return (
    <div className="flex flex-col items-center gap-lg">
      <div className="flex items-center gap-xl">
        <button
          aria-label="Stop timer"
          onClick={onStop}
          className="p-4 bg-card border border-border rounded-full text-text-secondary hover:text-text-primary transition-colors"
        >
          <Square size={24} fill="currentColor" />
        </button>

        <button
          aria-label={isActive ? "Pause timer" : "Start timer"}
          onClick={isActive ? onPause : onStart}
          className="w-20 h-20 flex items-center justify-center bg-white text-background rounded-full shadow-xl shadow-white/10 active:scale-95 transition-transform"
        >
          {isActive ? <Pause size={32} fill="currentColor" /> : <Play size={32} className="ml-1" fill="currentColor" />}
        </button>

        <button
          aria-label="Skip session"
          className="p-4 bg-card border border-border rounded-full text-text-secondary hover:text-text-primary transition-colors"
        >
          {/* Next/Skip button icon from design */}
          <div className="flex items-center">
            <Play size={20} fill="currentColor" />
            <div className="w-[2px] h-4 bg-current ml-[2px]" />
          </div>
        </button>
      </div>

      <div className="flex items-center gap-md">
        <Button variant="secondary" className="px-4 py-2 text-xs" onClick={() => onAdjust(5)}>
          <Plus size={14} className="mr-1" /> 5 MIN
        </Button>
        <Button variant="secondary" className="px-4 py-2 text-xs" onClick={() => onAdjust(-5)}>
          <Minus size={14} className="mr-1" /> 5 MIN
        </Button>
      </div>
    </div>
  );
};
